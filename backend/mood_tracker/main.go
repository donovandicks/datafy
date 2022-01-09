package main

import (
	"context"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/donovandicks/datafy/backend/mood-tracker/spotify"
	"github.com/donovandicks/datafy/backend/mood-tracker/telemetry"
)

// Handler is our lambda handler invoked by the `lambda.Start` function call
func Handler(ctx context.Context) (string, error) {
	logger := telemetry.InitLogger()
	defer logger.Sync()

	awsSession := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	spotify.AnalayzeTracks(awsSession)

	spotify.Authorize(awsSession)
	return "Function COMPLETED", nil
}

func main() {
	logger := telemetry.InitLogger()
	defer logger.Sync()
	logger.Info("Function TRIGGERED")

	lambda.Start(Handler)

	logger.Info("Function COMPLETED")
}
