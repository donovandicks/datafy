package aws

import (
	"fmt"

	"github.com/aws/aws-sdk-go/aws/awserr"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/secretsmanager"
	"github.com/donovandicks/datafy/backend/mood-tracker/telemetry"
	"go.uber.org/zap"
)

func GetSpotifySecrets(awsSession *session.Session, secretId *string) *secretsmanager.GetSecretValueOutput {
	logger := telemetry.InitLogger()
	defer logger.Sync()
	logger.Info("Retrieving AWS Secret", zap.String("id", *secretId))

	smanager := secretsmanager.New(awsSession)
	input := &secretsmanager.GetSecretValueInput{
		SecretId: secretId,
	}

	result, err := smanager.GetSecretValue(input)

	if err != nil {
		if awsError, ok := err.(awserr.Error); ok {
			panic(fmt.Sprint("Encountered an AWS Error when retrieving a secret: ", awsError.Error()))
		} else {
			panic(fmt.Sprint("Encountered an unexpected error when retrieving a secret: ", err.Error()))
		}
	}

	return result
}
