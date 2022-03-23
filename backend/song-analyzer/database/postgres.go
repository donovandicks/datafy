package database

import (
	"os"

	"github.com/donovandicks/datafy/backend/song-analyzer/spotify"
	"github.com/donovandicks/datafy/backend/song-analyzer/telemetry"
	"github.com/jackc/pgx"
	"go.uber.org/zap"
)

var logger = telemetry.InitLogger()

type Database struct {
	Conn *pgx.Conn
}

// `connect` establishes a connection to the Postgres database
func (db *Database) Connect() {
	logger.Info("Connecting to Postgres instance")
	config := pgx.ConnConfig{
		Host:     "localhost",
		Port:     5432,
		Database: "datafy",
	}
	conn, err := pgx.Connect(config)
	if err != nil {
		logger.Error("Unable to connect to database", zap.Any("error", err))
		os.Exit(1)
	}

	db.Conn = conn
}

func (db *Database) GetRowsMissingDetail() *pgx.Rows {
	logger.Info("Retrieving tracks without detailed data")
	rows, err := db.Conn.Query(`
	SELECT track.track_id
	FROM track
	LEFT JOIN track_detail USING (track_id)
	WHERE track_detail.track_id IS NULL;
	`)
	if err != nil {
		logger.Error("Failed to retrieve tracks missing detailed data", zap.Any("error", err))
		os.Exit(1)
	}

	return rows
}

func UnmarshalRows[T any](rows *pgx.Rows, target *[]T) {
	logger.Info("Unmarshalling rows")
	for rows.Next() {
		var item T
		err := rows.Scan(&item)
		if err != nil {
			logger.Error("Failed to scan row", zap.Any("error", err))
		}
		*target = append(*target, item)
	}
}

func (db *Database) InsertTrackDetail(row *spotify.TrackInfo) {
	db.Conn.Exec(
		`INSERT INTO track_detail
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)`,
		row.Id,
		row.Acousticness,
		row.Danceability,
		row.Duration,
		row.Energy,
		row.Instrumentalness,
		row.Loudness,
		row.Speechiness,
		row.Tempo,
		row.Valence,
	)
}
