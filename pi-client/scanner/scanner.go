package main

import (
    "fmt"
    "flag"
    "bytes"
    "net/http"
    "encoding/json"

    "github.com/peterhellberg/acr122u"
)

// Entpoint for client
var endpoint string

type User struct {
    SerialNr string `json:"serialNr"`
    SpotNr string `json:"spotNr"`
}

func post(cardInfo []byte) {
    // Sends POST request to REST api
    resp, err := http.Post(
        endpoint, 
        "application/json; charset=utf-8", 
        bytes.NewBuffer(cardInfo),
    )

    if err != nil {
        fmt.Println(err)
        return
    }

    resp.Body.Close()

    if resp.StatusCode != 201 {
        fmt.Println("Error! Try again or contact appropriate staff.") 
    }
}

func main() {
    // Take endpoint from user with a flag
    flag.StringVar(&endpoint, "endpoint", "", "set the desired endpoint for the client")
    flag.Parse()
    
    // Establish new context for card reader
    ctx, err := acr122u.EstablishContext()
    if err != nil {
        panic(err)
    }

    // Marshal card UID and nfc scanner number
    ctx.ServeFunc(func(card acr122u.Card) {
        cardInfo, err := json.Marshal(User{
            SerialNr: string(card.UID()),
            SpotNr: card.Reader(),
        })

        if err != nil {
            panic(err)
        }

        // take card info and post it
        post(cardInfo)
    })
}

