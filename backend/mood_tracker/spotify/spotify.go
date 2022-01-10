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
	"sync"

	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
	dynamo "github.com/donovandicks/datafy/backend/mood-tracker/aws"
	smanager "github.com/donovandicks/datafy/backend/mood-tracker/aws"
	"github.com/donovandicks/datafy/backend/mood-tracker/telemetry"
	"go.uber.org/zap"
)

var logger = telemetry.InitLogger()

type Secrets struct {
	ClientId string `json:"spotify_client_id"`
	Secret   string `json:"spotify_secret"`
}

type AccessToken struct {
	Token     string `json:"access_token"`
	Type      string `json:"token_type"`
	ExpiresIn int    `json:"expires_in"`
}

type SongInfo struct {
	Id     string  `json:"id"`
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
	defer logger.Sync()
	logger.Info("Authorizing with Spotify")

	secrets := getSecrets(awsSession)
	token := getAccessToken(secrets)

	return token.Token
}

func getSongInfo(token string, trackId string) SongInfo {
	defer logger.Sync()
	logger.Info("Retrieving Track Info", zap.String("songId", trackId))
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
		logger.Error("Failed to Execute Request", zap.String("error", err.Error()))
		panic(fmt.Sprint("Failed to Execute Request: ", err.Error()))
	}

	defer res.Body.Close()
	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		logger.Error("Failed to Read Response Body", zap.String("error", err.Error()))
		panic(fmt.Sprint("Failed to Read Response Body: ", err.Error()))
	}

	info := SongInfo{}
	err = json.Unmarshal([]byte(string(body)), &info)
	if err != nil {
		logger.Error("Failed to Unmarshal Response Body", zap.String("error", err.Error()))
		panic(fmt.Sprint("Failed to Unmarshal Response Body: ", err.Error()))
	}

	logger.Info("Retrieved Track Info", zap.String("songId", trackId))
	return info
}

func getTotalPlayCount(songs []Song) int {
	totalPlays := 0
	for _, song := range songs {
		totalPlays += song.Count
	}
	logger.Info("Total Play Count", zap.Int("count", totalPlays))
	return totalPlays
}

func analayzeTracks(awsSession *session.Session, wg *sync.WaitGroup, songs []Song, infoChan chan SongInfo) {
	defer logger.Sync()
	token := authorize(awsSession)

	for _, song := range songs {
		wg.Add(1)
		go func(id string) {
			defer wg.Done()
			select {
			case infoChan <- getSongInfo(token, id):
			default:
			}
		}(song.Id)
	}
}

func GetMeanWeightedEnergy(awsSession *session.Session, wg *sync.WaitGroup) {
	dynamoClient := dynamodb.New(awsSession)
	tableName := os.Getenv("SPOTIFY_TRACKS_TABLE")
	songs := getSongsPlayedInLastWeek(dynamoClient, tableName)
	totalPlays := getTotalPlayCount(songs)

	infoChan := make(chan SongInfo, len(songs))
	analayzeTracks(awsSession, wg, songs, infoChan)

	weightedEnergy := 0.0
	for range songs {
		info := <-infoChan
		logger.Info("Info from Channel", zap.Any("info", info))

		weight := 0.0
		for _, song := range songs {
			if song.Id == info.Id {
				weight = float64(song.Count) / float64(totalPlays)
				break
			}
		}

		if weight == 0.0 {
			logger.Warn("Failed to Find Match", zap.String("songId", info.Id))
			continue
		}

		weightedEnergy += weight * info.Energy
	}

	meanWeightedEnergy := weightedEnergy / float64(len(songs))
	logger.Info("Calculated Mean Weighted Energy", zap.Float64("energy", meanWeightedEnergy))
}
