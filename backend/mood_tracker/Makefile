.PHONY: build clean deploy

build:
	env GOARCH=amd64 GOOS=linux go build -ldflags="-s -w" -o bin/mood-tracker main.go

clean:
	rm -rf ./bin

tidy:
	go mod tidy

deploy: clean build
	sls deploy --verbose

run: clean build
	serverless invoke local -f mood-tracker
