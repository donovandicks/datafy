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

	if !rows.Next() {
		logger.Info("No track IDs retrieved, database up-to-date.")
		return
	}

	var trackIds []string
	database.UnmarshalRows(rows, &trackIds)

	logger.Info("Retrieved track IDs", zap.Strings("trackIds", trackIds))

	token := spotify.Authorize()

	for _, id := range trackIds {
		info := spotify.GetTrackInfo(token, id)
		db.InsertTrackDetail(&info)
	}
}
