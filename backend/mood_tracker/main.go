package main

import (
	"context"
	"sync"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/donovandicks/datafy/backend/mood-tracker/spotify"
	"github.com/donovandicks/datafy/backend/mood-tracker/telemetry"
)

var logger = telemetry.InitLogger()
var wg sync.WaitGroup

// Handler is our lambda handler invoked by the `lambda.Start` function call
func Handler(ctx context.Context) (string, error) {
	defer logger.Sync()

	awsSession := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	spotify.GetMeanWeightedEnergy(awsSession, &wg)

	wg.Wait()
	return "Handler Exiting", nil
}

func main() {
	defer logger.Sync()

	logger.Info("Function TRIGGERED")
	lambda.Start(Handler)
	logger.Info("Function COMPLETED")
}
