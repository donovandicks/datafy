package spotify

import (
	b64 "encoding/base64"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"strings"

	"github.com/joho/godotenv"
)

type AccessToken struct {
	Token     string `json:"access_token"`
	Type      string `json:"token_type"`
	ExpiresIn int    `json:"expires_in"`
}

type Secrets struct {
	ClientId string
	Secret   string
}

func getSecrets() Secrets {
	err := godotenv.Load()
	if err != nil {
		logger.Fatal("Error loading .env file")
	}

	clientId := os.Getenv("SPOTIFY_CLIENT_ID")
	secret := os.Getenv("SPOTIFY_CLIENT_SECRET")
	return NewSecrets(clientId, secret)
}

func NewSecrets(clientId string, secret string) Secrets {
	sc := Secrets{}
	sc.ClientId = clientId
	sc.Secret = secret

	return sc
}

func Authorize() string {
	defer logger.Sync()
	logger.Info("Authorizing with Spotify")

	secrets := getSecrets()
	token := getAccessToken(&secrets)

	return token.Token
}

func getAccessToken(secrets *Secrets) AccessToken {
	endpoint := "https://accounts.spotify.com/api/token"
	b64secret := b64.StdEncoding.EncodeToString([]byte(fmt.Sprintf("%s:%s", secrets.ClientId, secrets.Secret)))

	data := url.Values{}
	data.Set("grant_type", "client_credentials")

	client := &http.Client{}
	req, err := http.NewRequest("POST", endpoint, strings.NewReader(data.Encode()))
	if err != nil {
		panic(fmt.Sprint("Failed to Create New Request: ", err.Error()))
	}

	req.Header.Add("Content-Type", "application/x-www-form-urlencoded")
	req.Header.Add("Authorization", fmt.Sprintf("Basic %s", b64secret))

	res, err := client.Do(req)
	if err != nil {
		panic(fmt.Sprint("Failed to Execute Request: ", err.Error()))
	}

	defer res.Body.Close()
	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		panic(fmt.Sprint("Failed to Read Response Body: ", err.Error()))
	}

	token := AccessToken{}
	err = json.Unmarshal([]byte(string(body)), &token)
	if err != nil {
		panic(fmt.Sprint("Failed to Unmarshal Response Body: ", err.Error()))
	}

	logger.Info("Retrieved Access Token")
	return token
}
