package analysis

import (
	"github.com/donovandicks/datafy/sherlock/database"
	"github.com/donovandicks/datafy/sherlock/telemetry"
	"go.uber.org/zap"
)

var logger = telemetry.InitLogger()

func CompareTracks(track1 database.Track, track2 database.Track) {
	energyDiff := track1.Energy - track2.Energy
	logger.Info("Energy Differences", zap.Float64("energyDiff", energyDiff))
}
