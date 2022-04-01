package main

import (
	"github.com/donovandicks/datafy/sherlock/analysis"
	"github.com/donovandicks/datafy/sherlock/database"
	"github.com/donovandicks/datafy/sherlock/telemetry"
	"go.uber.org/zap"
)

var logger = telemetry.InitLogger()

func main() {
	db := database.Database{}
	db.Connect()

	id1 := "2Im64pIz6m0EJKdUe6eZ8r"
	id2 := "00iYCxpoIxtyBr2JzhIpxx"
	tracks := db.GetRowsToCompare(id1, id2)
	logger.Info("Features", zap.Any("features", tracks))

	analysis.CompareTracks((*tracks)[0], (*tracks)[1])
}
