package main

import (
	"github.com/donovandicks/datafy/oracle/database"
	"github.com/donovandicks/datafy/oracle/spotify"
	"github.com/donovandicks/datafy/oracle/telemetry"
	"go.uber.org/zap"
)

var logger = telemetry.InitLogger()

func main() {
	db := database.Database{}
	db.Connect()
	defer db.Conn.Close()

	rows := db.GetRowsMissingDetail()

	var trackIds []string
	database.UnmarshalRows(rows, &trackIds)

	if len(trackIds) == 0 {
		logger.Info("No tracks to analyze")
		return
	}

	logger.Info("Retrieved track IDs", zap.Strings("trackIds", trackIds))

	token := spotify.Authorize()

	for _, id := range trackIds {
		rawTrack := spotify.GetTrack(token, id)
		audio := spotify.GetTrackAudioFeatures(token, id)

		db.InsertArtist(rawTrack)
		db.InsertAlbum(rawTrack)

		info := spotify.TrackInfo{RawTrack: *rawTrack, AudioFeatures: *audio}
		db.InsertTrackDetail(&info)
	}
}
