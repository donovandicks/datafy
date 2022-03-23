package spotify

import (
	"fmt"
	"net/http"

	"github.com/donovandicks/datafy/backend/song-analyzer/net"
	"github.com/donovandicks/datafy/backend/song-analyzer/telemetry"
	"go.uber.org/zap"
)

var logger = telemetry.InitLogger()

type TrackInfo struct {
	Id               string  `json:"id"`
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

func GetTrackInfo(token string, trackId string) TrackInfo {
	defer logger.Sync()
	logger.Info("Retrieving Track Info", zap.String("trackId", trackId))

	endpoint := fmt.Sprintf("https://api.spotify.com/v1/audio-features/%s", trackId)
	req := net.CreateRequest("GET", endpoint, token)

	client := &http.Client{}
	res := net.MakeRequest(client, req)

	defer res.Body.Close()
	body := net.ReadResponse(res)

	var info TrackInfo
	net.ParseResponse(body, &info)

	return info
}
