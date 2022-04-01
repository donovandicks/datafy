package net

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"

	"github.com/donovandicks/datafy/oracle/telemetry"
	"go.uber.org/zap"
)

var logger = telemetry.InitLogger()

func CreateRequest(method string, endpoint string, token string) *http.Request {
	req, err := http.NewRequest(method, endpoint, strings.NewReader(""))
	if err != nil {
		panic(fmt.Sprint("Failed to Create New Request: ", err.Error()))
	}

	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("Authorization", fmt.Sprintf("Bearer %s", token))
	return req
}

func MakeRequest(client *http.Client, request *http.Request) *http.Response {
	res, err := client.Do(request)
	if err != nil {
		logger.Error("Failed to Execute Request", zap.Error(err))
		panic(fmt.Sprint("Failed to Execute Request: ", err.Error()))
	}
	return res
}

func ReadResponse(response *http.Response) []byte {
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		logger.Error("Failed to Read Response Body", zap.Error(err))
		panic(fmt.Sprint("Failed to Read Response Body: ", err.Error()))
	}

	return body
}

func ParseResponse[T any](body []byte, target *T) {
	err := json.Unmarshal([]byte(string(body)), target)
	if err != nil {
		logger.Error("Failed to Unmarshal Response Body", zap.Error(err))
		panic(fmt.Sprint("Failed to Unmarshal Response Body: ", err.Error()))
	}
}
