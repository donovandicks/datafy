package spotify

import (
	"fmt"
	"net/http"

	"github.com/donovandicks/datafy/oracle/net"
	"github.com/donovandicks/datafy/oracle/telemetry"
	"go.uber.org/zap"
)

var logger = telemetry.InitLogger()

type TrackInfo struct {
	RawTrack
	AudioFeatures
}

type AudioFeatures struct {
	Acousticness     float64 `json:"acousticness"`
	Danceability     float64 `json:"danceability"`
	Duration         int64   `json:"duration_ms"`
	Energy           float64 `json:"energy"`
	Instrumentalness float64 `json:"instrumentalness"`
	Loudness         float64 `json:"loudness"`
	Speechiness      float64 `json:"speechiness"`
	Tempo            float64 `json:"tempo"`
	Valence          float64 `json:"valence"`
}

type RawTrack struct {
	Id         string `json:"id"`
	Name       string `json:"name"`
	Popularity int64  `json:"popularity"`
	Album      struct {
		Id   string `json:"id"`
		Name string `json:"name"`
	} `json:"album"`
	Artists []struct {
		Id   string `json:"id"`
		Name string `json:"name"`
	} `json:"artists"`
}

func GetTrackAudioFeatures(token string, trackId string) *AudioFeatures {
	defer logger.Sync()
	logger.Info("Retrieving track audio features", zap.String("trackId", trackId))

	endpoint := fmt.Sprintf("https://api.spotify.com/v1/audio-features/%s", trackId)
	req := net.CreateRequest("GET", endpoint, token)

	client := &http.Client{}
	res := net.MakeRequest(client, req)

	defer res.Body.Close()
	body := net.ReadResponse(res)

	var features AudioFeatures
	net.ParseResponse(body, &features)

	return &features
}

func GetTrack(token string, trackId string) *RawTrack {
	defer logger.Sync()
	logger.Info("Retrieving track", zap.String("trackId", trackId))

	endpoint := fmt.Sprintf("https://api.spotify.com/v1/tracks/%s", trackId)
	req := net.CreateRequest("GET", endpoint, token)

	client := &http.Client{}
	res := net.MakeRequest(client, req)

	defer res.Body.Close()
	body := net.ReadResponse(res)

	var raw RawTrack
	net.ParseResponse(body, &raw)
	return &raw
}
