package account

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"net/url"
	"strings"
)

type User struct {
	Token  string `json:"token"`
	UserId string `json:"user_id"`
}

func LoginFromFile(filename string) User {
	email, pass := getEmailAndPass(filename)
	return getUserAndToken(email, pass)
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func getUserAndToken(email string, password string) User {
	response, err := http.PostForm("https://iot.seeed.cc/v1/user/login?email",
		url.Values{"email": {email}, "password": {password}})
	defer response.Body.Close()
	check(err)

	if response.StatusCode != 200 {
		panic("Status is " + response.Status + " aborting!")
	}

	body, errd := ioutil.ReadAll(response.Body)
	check(errd)

	var user User
	er := json.Unmarshal(body, &user)
	check(er)
	return user
}

// getEmailAndPass takes the file location where your email and password
// are stored (space delimited {email pass} ) and returns them as variables.
func getEmailAndPass(file_loc string) (string, string) {
	dat, err := ioutil.ReadFile(file_loc)
	check(err)
	string_data := strings.Split(string(dat), " ")
	return string_data[0], string_data[1]
}
