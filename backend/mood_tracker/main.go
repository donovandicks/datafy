package main

import (
	"context"
	"fmt"
	"os"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/dynamodbattribute"
)

type Song struct {
	Id    string `json:"track_id"`
	Count int    `json:"play_count"`
}

// Handler is our lambda handler invoked by the `lambda.Start` function call
func Handler(ctx context.Context) (string, error) {
	aws_session := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	dynamo_client := dynamodb.New(aws_session)

	table_name := os.Getenv("SPOTIFY_TRACKS_TABLE")

	result, err := dynamo_client.Scan(&dynamodb.ScanInput{
		TableName: aws.String(table_name),
	})

	if err != nil {
		fmt.Println(err.Error())
		panic(fmt.Sprint("Failed to scan DynamoDB table: ", table_name))
	}

	var songs []Song

	err = dynamodbattribute.UnmarshalListOfMaps(result.Items, &songs)

	if err != nil {
		panic(fmt.Sprint("Failed to unmarshal DynamoDB data: ", err))
	}

	return fmt.Sprint("Results: ", songs), nil
}

func main() {
	lambda.Start(Handler)
}
