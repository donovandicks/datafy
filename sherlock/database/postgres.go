package database

import (
	"os"

	"github.com/donovandicks/datafy/sherlock/telemetry"
	"go.uber.org/zap"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var logger = telemetry.InitLogger()

type Database struct {
	Conn *gorm.DB
}

type Track struct {
	Id               string
	Name             string
	ArtistId         string
	AlbumId          string
	Popularity       int
	Acousticness     float64
	Danceability     float64
	Duration         int `gorm:"column:duration_ms"`
	Energy           float64
	Instrumentalness float64
	Loudness         float64
	Speechiness      float64
	Tempo            float64
	Valence          float64
}

type Tabler interface {
	TableName() string
}

// TableName overrides the table name used by Track to `track`
func (Track) TableName() string {
	return "track"
}

// `connect` establishes a connection to the Postgres database
func (db *Database) Connect() {
	logger.Info("Connecting to Postgres instance")

	dsn := "host=localhost dbname=datafy port=5432"
	conn, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})

	if err != nil {
		logger.Error("Unable to connect to database", zap.Error(err))
		os.Exit(1)
	}

	db.Conn = conn
}

func (db *Database) GetTrack(trackId1 string) *Track {
	var track Track
	result := db.Conn.Where("id = ?", trackId1).Find(&track)

	err := result.Error
	if err != nil {
		logger.Error("Failed to query database", zap.Error(err))
	}

	return &track
}

func (db *Database) GetRowsToCompare(trackId1 string, trackId2 string) *[]Track {
	var tracks []Track
	result := db.Conn.Where("id = ?", trackId1).Or("id = ?", trackId2).Find(&tracks)

	err := result.Error
	if err != nil {
		logger.Error("Failed to query database", zap.Error(err))
	}

	return &tracks
}
