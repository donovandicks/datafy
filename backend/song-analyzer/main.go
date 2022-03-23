package main

import (
	"github.com/donovandicks/datafy/backend/song-analyzer/database"
	"github.com/donovandicks/datafy/backend/song-analyzer/spotify"
	"github.com/donovandicks/datafy/backend/song-analyzer/telemetry"
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
		logger.Info("No track IDs retrieved, database up-to-date.")
		return
	}

	logger.Info("Retrieved track IDs", zap.Strings("trackIds", trackIds))

	token := spotify.Authorize()

	for _, id := range trackIds {
		info := spotify.GetTrackInfo(token, id)
		db.InsertTrackDetail(&info)
	}
}
