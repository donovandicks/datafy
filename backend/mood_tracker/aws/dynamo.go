package aws

import (
	"fmt"
	"log"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/service/dynamodb"
	"github.com/aws/aws-sdk-go/service/dynamodb/expression"
	"github.com/donovandicks/datafy/backend/mood-tracker/telemetry"
	"go.uber.org/zap"
)

func buildOneWeekAgoFilter() expression.Expression {
	oneWeekAgo := time.Now().AddDate(0, 0, -7).Unix()
	log.Println("One Week Ago: ", oneWeekAgo)

	filter := expression.
		Name("last_played_timestamp").
		GreaterThanEqual(expression.Value(oneWeekAgo))

	expr, err := expression.NewBuilder().WithFilter(filter).Build()

	if err != nil {
		panic(fmt.Sprint("Failed to build scan filter: ", err.Error()))
	}

	log.Println("Built Expression: ", expr)
	return expr
}

// ScanTable accepts a DynamoDB client and the name of a DynamoBD table and
// returns the items found from running a scan on that table.
func ScanTable(
	client *dynamodb.DynamoDB,
	tableName string,
) []map[string]*dynamodb.AttributeValue {
	logger := telemetry.InitLogger()
	defer logger.Sync()
	logger.Info("Scanning Dynamo Table", zap.String("tableName", tableName))

	filterExpr := buildOneWeekAgoFilter()

	result, err := client.Scan(&dynamodb.ScanInput{
		TableName:                 aws.String(tableName),
		FilterExpression:          filterExpr.Filter(),
		ExpressionAttributeNames:  filterExpr.Names(),
		ExpressionAttributeValues: filterExpr.Values(),
	})

	if err != nil {
		logger.Error(err.Error())
		panic(fmt.Sprint("Failed to scan DynamoDB table: ", tableName))
	}

	return result.Items
}
