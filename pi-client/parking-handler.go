package main

import (
	"log"
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
	
	// Bind the incomming JSON to struct spot
	err := context.BindJSON(&spot)
	if err != nil {
		return
	}
	
	// Return http 201 CREATED
	context.IndentedJSON(http.StatusCreated, spot)

	parkingSpot(spot)
}

func changeLed(number int, occupied bool) {
	// Create pin with given GPIO pin
	pin := rpio.Pin(number)

	// Info needs to be sent out
	pin.Output()
	
	// Turn on/off if occupied or not
	if occupied {
		pin.High()
	} else {
		pin.Low()
	}
}

func parkingSpot(spot Spot) {
	numbers := map[int]int{12:1, 16:2, 20:3, 21:4, 26:5, 19:6, 13:7, 6:8}
	
	// Changing the values for the appropriate parking spot
	for number := range numbers {
		if spot.Number == number {
			changeLed(spot.Number, spot.Occupied)
		}
	}
}

func parkingHandlerManager() {
	// Open memory range for GPIO access 
	err := rpio.Open()
	if err != nil {
		log.Println(err)
	}

	router := gin.Default()

	// Run postSpot func on call /pin
	router.POST("/pin", postSpot)
	
	// Start listening on port 8080
	router.Run(":8080")

	// Close the memory range at program shutdown
	rpio.Close()
}

