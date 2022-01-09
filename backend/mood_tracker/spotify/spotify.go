package spotify

import (
	b64 "encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"strings"

	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
	dynamo "github.com/donovandicks/datafy/backend/mood-tracker/aws"
	smanager "github.com/donovandicks/datafy/backend/mood-tracker/aws"
	"github.com/donovandicks/datafy/backend/mood-tracker/telemetry"
	"go.uber.org/zap"
)

type Secrets struct {
	ClientId string `json:"spotify_client_id"`
	Secret   string `json:"spotify_secret"`
}

type AccessToken struct {
	Token     string `json:"access_token"`
	Type      string `json:"token_type"`
	ExpiresIn int    `json:"expires_in"`
}

type TrackInfo struct {
	Energy float64 `json:"energy"`
}

type Song struct {
	Id    string `json:"track_id"`
	Count int    `json:"play_count"`
}

// GetSongsPlayedInLastWeek accepts a DynamoDB client and the name of a DynamoDB
// table and returns a list of `Song`s from the table that were played within the
// last 7 days.
func getSongsPlayedInLastWeek(client *dynamodb.DynamoDB, tableName string) []Song {
	logger := telemetry.InitLogger()
	defer logger.Sync()
	logger.Info("Retrieving Songs Played Within Last Week")

	var songs []Song
	items := dynamo.ScanTable(client, tableName)

	err := dynamodbattribute.UnmarshalListOfMaps(items, &songs)
	if err != nil {
		panic(fmt.Sprint("Failed to unmarshal DynamoDB data: ", err.Error()))
	}

	logger.Info("Retrieved Songs", zap.Int("count", len(songs)))
	return songs
}

func getSecrets(awsSession *session.Session) *Secrets {
	logger := telemetry.InitLogger()
	defer logger.Sync()

	logger.Info("Retrieving Spotify Secrets")
	secretId := os.Getenv("SPOTIFY_SECRETS")
	secretString := smanager.GetSpotifySecrets(awsSession, &secretId).SecretString

	secrets := Secrets{}
	json.Unmarshal([]byte(*secretString), &secrets)

	logger.Info("Retrieved Secrets")
	return &secrets
}

func getAccessToken(secrets *Secrets) AccessToken {
	logger := telemetry.InitLogger()
	defer logger.Sync()

	endpoint := "https://accounts.spotify.com/api/token"
	b64secret := b64.StdEncoding.EncodeToString([]byte(fmt.Sprintf("%s:%s", secrets.ClientId, secrets.Secret)))

	data := url.Values{}
	data.Set("grant_type", "client_credentials")

	client := &http.Client{}
	req, err := http.NewRequest("POST", endpoint, strings.NewReader(data.Encode()))
	if err != nil {
		panic(fmt.Sprint("Failed to Create New Request: ", err.Error()))
	}

	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
	req.Header.Add("Authorization", fmt.Sprintf("Basic %s", b64secret))

	res, err := client.Do(req)
	if err != nil {
		panic(fmt.Sprint("Failed to Execute Request: ", err.Error()))
	}

	defer res.Body.Close()
	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		panic(fmt.Sprint("Failed to Read Response Body: ", err.Error()))
	}

	token := AccessToken{}
	err = json.Unmarshal([]byte(string(body)), &token)
	if err != nil {
		panic(fmt.Sprint("Failed to Unmarshal Response Body: ", err.Error()))
	}

	logger.Info("Retrieved Access Token")
	return token
}

func authorize(awsSession *session.Session) string {
	logger := telemetry.InitLogger()
	defer logger.Sync()
	logger.Info("Authorizing with Spotify")

	secrets := getSecrets(awsSession)
	token := getAccessToken(secrets)

	return token.Token
}

func getTrackInfo(token string, trackId string) TrackInfo {
	endpoint := fmt.Sprintf("https://api.spotify.com/v1/audio-features/%s", trackId)
	client := &http.Client{}
	req, err := http.NewRequest("GET", endpoint, strings.NewReader(""))
	if err != nil {
		panic(fmt.Sprint("Failed to Create New Request: ", err.Error()))
	}

	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("Authorization", fmt.Sprintf("Bearer %s", token))

	res, err := client.Do(req)
	if err != nil {
		panic(fmt.Sprint("Failed to Execute Request: ", err.Error()))
	}

	defer res.Body.Close()
	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		panic(fmt.Sprint("Failed to Ready Response Body: ", err.Error()))
	}

	info := TrackInfo{}
	err = json.Unmarshal([]byte(string(body)), &info)
	if err != nil {
		panic(fmt.Sprint("Failed to Unmarshal Response Body: ", err.Error()))
	}

	return info
}

func getAllTrackInfo(songs []Song, token string) []TrackInfo {
	logger := telemetry.InitLogger()
	defer logger.Sync()

	logger.Info("Analyzing Tracks", zap.Int("count", len(songs)))
	infoChannel := make(chan TrackInfo)
	for _, song := range songs {
		go func(id string) {
			info := getTrackInfo(token, id)
			infoChannel <- info
		}(song.Id)
	}

	var songsInfo []TrackInfo
	for range songs {
		info := <-infoChannel
		songsInfo = append(songsInfo, info)
	}

	logger.Info("Analyzed Tracks", zap.Int("count", len(songsInfo)))
	return songsInfo
}

func AnalayzeTracks(awsSession *session.Session) {
	logger := telemetry.InitLogger()
	defer logger.Sync()

	dynamoClient := dynamodb.New(awsSession)
	tableName := os.Getenv("SPOTIFY_TRACKS_TABLE")
	songs := getSongsPlayedInLastWeek(dynamoClient, tableName)
	token := authorize(awsSession)

	songsInfo := getAllTrackInfo(songs, token)

	meanEnergy := 0.0
	for _, info := range songsInfo {
		meanEnergy += info.Energy
	}

	logger.Info("Calculated Mean Energy", zap.Float64("meanEnergy", meanEnergy/float64(len(songsInfo))))
}
