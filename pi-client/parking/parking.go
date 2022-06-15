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
	// Changing the values for the appropriate parking spot
	switch spot.Number {
		case 1:
			changeLed(12, spot.Occupied)
		case 2:
			changeLed(16, spot.Occupied)
		case 3:
			changeLed(20, spot.Occupied)
		case 4:
			changeLed(21, spot.Occupied)
		case 5:
			changeLed(26, spot.Occupied)
		case 6:
			changeLed(19, spot.Occupied)
		case 7:
			changeLed(13, spot.Occupied)
		case 8:
			changeLed(6, spot.Occupied)
	}
}

func main() {
	// Open memory range for GPIO access on /dev/mem.
	// Keeps the pin configuration on shutdown too
	err := rpio.Open()
	if err != nil {
		log.Println(err)
	}

	router := gin.Default()

	// Run postSpot func on call /pin
	router.POST("/pin", postSpot)
	
	// Start listening on port 8080
	router.Run(":8080")
}

