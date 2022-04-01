package database

import (
	"os"

	"github.com/donovandicks/datafy/oracle/spotify"
	"github.com/donovandicks/datafy/oracle/telemetry"
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
		logger.Error("Unable to connect to database", zap.Error(err))
		os.Exit(1)
	}

	db.Conn = conn
}

func (db *Database) GetRowsMissingDetail() *pgx.Rows {
	logger.Info("Retrieving tracks without detailed data")
	rows, err := db.Conn.Query(`
	SELECT
		pc.track_id
	FROM
		playcount AS pc
		LEFT JOIN track ON pc.track_id = track.id
	WHERE
		track.id IS NULL;
	`)
	if err != nil {
		logger.Error("Failed to retrieve tracks missing detailed data", zap.Error(err))
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
			logger.Error("Failed to scan row", zap.Error(err))
		}
		*target = append(*target, item)
	}
}

func (db *Database) InsertArtist(row *spotify.RawTrack) {
	_, err := db.Conn.Exec(`
	INSERT INTO
		artist
		(id, name)
	VALUES
		($1, $2)
	`,
		row.Artists[0].Id,
		row.Artists[0].Name,
	)

	if err != nil {
		logger.Error("Error during artist insertion", zap.Error(err))
		return
	}
}

func (db *Database) InsertAlbum(row *spotify.RawTrack) {
	_, err := db.Conn.Exec(`
	INSERT INTO
		album
		(id, name)
	VALUES
		($1, $2)
	`,
		row.Album.Id,
		row.Album.Name,
	)

	if err != nil {
		logger.Error("Error during album insertion", zap.Error(err))
		return
	}
}

func (db *Database) InsertTrackDetail(row *spotify.TrackInfo) {
	_, err := db.Conn.Exec(`
		INSERT INTO
			track
			(id, name, album_id, artist_id, acousticness, danceability, duration_ms,
				energy, instrumentalness, loudness, popularity, speechiness, tempo,
				valence)
		VALUES
			($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
		`,
		row.Id,
		row.Name,
		row.Album.Id,
		row.Artists[0].Id,
		row.Acousticness,
		row.Danceability,
		row.Duration,
		row.Energy,
		row.Instrumentalness,
		row.Loudness,
		row.Popularity,
		row.Speechiness,
		row.Tempo,
		row.Valence,
	)

	if err != nil {
		logger.Error("Error during track insertion", zap.Error(err))
		return
	}
}
