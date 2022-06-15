package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/stianeikeland/go-rpio/v4"
)

type Spot struct {
	Type 		string	`json:"type"`
	Number 		int		`json:"number"`
	Occupied	bool	`json:"occupied"`
}

func postSpot(context *gin.Context) {
	var spot Spot

	err := context.BindJSON(&spot)
	if err != nil {
		return
	}

	context.IndentedJSON(http.StatusCreated, spot)
	parkingSpot(spot)
}

func router() {
	router := gin.Default()
	router.POST("/pin", postSpot)

	router.Run(":8080")
}

func changeLed(number int, occupied bool) {
	pin := rpio.Pin(number)
	pin.Mode(rpio.Output)
	
	if occupied {
		pin.Write(rpio.High)
	} else {
		pin.Write(rpio.Low)
	}
}

func parkingSpot(spot Spot) {
	switch spot.Number {
		case 12:
			changeLed(spot.Number, spot.Occupied)
		case 16:
			changeLed(spot.Number, spot.Occupied)
		case 20:
			changeLed(spot.Number, spot.Occupied)
		case 21:
			changeLed(spot.Number, spot.Occupied)
		case 26:
			changeLed(spot.Number, spot.Occupied)
		case 19:
			changeLed(spot.Number, spot.Occupied)
		case 13:
			changeLed(spot.Number, spot.Occupied)
		case 6:
			changeLed(spot.Number, spot.Occupied)
		default:
			fmt.Println("Error")
	}
}
