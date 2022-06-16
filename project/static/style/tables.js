const maxRows = 2;
const maxColumns = 4;
const maxSpots = 8;

var table_guests = document.getElementById('parking-guests');
var table_staff = document.getElementById('parking-staff');
var table_students = document.getElementById('parking-students');
var occupied_check = document.getElementById('check_occupied');

let checking = false;

// Transform the spots JSON variable into an array
var parking_spots = JSON.parse(spots);


tableCreate(table_staff, 'Staff');
tableCreate(table_students, 'Student');
tableCreate(table_guests, 'Guest');

occupied_check.addEventListener('change', function() {

  sendInfo = {
    type: 'Guest',
    number: 2,
    occupied: true
  }

  $.ajax({
    type: "POST",
    url: "10.108.149.14:8080/pin",
    dataType: "json",
    success: function (msg) {
        if (msg) {

      
        } else {

        }
    },
    data: sendInfo
});

  if (this.checked) {
    console.log("Checkbox is checked..");
  } else {
    console.log("Checkbox is not checked..");
  }
});

function tableCreate(table, type){

  var sortedArray = parking_spots.filter(spot => spot.type === type)

  // Order the list based on spot number
  sortedArray.sort((a, b) => (a.number > b.number) ? 1 : -1)

  var tr1 = table.insertRow();  
  var tr2 = table.insertRow();
  var index = 0;

  for(var i = 0; i < 4; i++){

    addTableCell(sortedArray[index], tr1);
    index++;
    addTableCell(sortedArray[index], tr2);
    index++;
    }

}

function editSpotStatus(cell, occupied) {
    if(occupied) {
      var imageAddress = "url('../static/style/Images/" + getRandomCarImage() + "')"
      cell.style.backgroundImage = imageAddress;
    } else {
    	cell.style.backgroundImage = '';
    }
}

  function addTableCell(spot, row) {
    var td = row.insertCell();
    td.classList.add("park-spot");
    td.onclick = function () {
      tableCellClick(spot,td);
    }; 

	editSpotStatus(td, spot.occupied);
  }

  // Action to be performed by clicking on a parking spot
  function tableCellClick(spot, el){
    // Finds the previous active spot if any
    let prevActive = document.querySelector(".active");
    let sideBox = document.querySelector("#sideBar");

    // if any previous active spot is remove
    if (prevActive != undefined) {
      prevActive.classList.remove("active");
    }
    else {
      // Adds event listener to hide info box and remove active spot when not clicking on spots
      document.querySelector("#parkingLot").addEventListener("click", function(e){
        if (!e.target.classList.contains("park-spot") && sideBox.classList != '') {
          sideBox.classList.remove("shown");
          document.querySelector(".active").classList.remove("active"); 
        }
      })
    }
    // Shows the info box if not already shown
    if (!sideBox.classList.contains("shown")) {
       sideBox.classList.add("shown");
    }
    // Adds active calss to the element to shown whick spot was clicked
    el.classList.add("active");
    // Display the parking spot info in the info box
    showParkSpotInfo(spot);
    console.log(spot);
  }

let roleBox = document.querySelector("#infoBoxRole h2");
let numberBox = document.querySelector("#infoBoxNumber h2");
let freeStatus = document.querySelector("#infoBoxTaken h2");

  function showParkSpotInfo(spot) {
    roleBox.innerHTML = spot.type;
    numberBox.innerHTML = spot.number;
    // Checks if the spot is taken
    if (spot.occupied) {
      occupied_check.checked = true;
    }
    else {
      occupied_check.checked = false;
    }
  }

  function getRandomCarImage(){
    var rnd = Math.floor(Math.random() * 10) + 1;
    return 'car' + rnd + '.png';
  }


// Checking for updates between database and existing spots
let newSpots;

function CheckSpots() {
	// GET updated parking spots
	$.ajax({
		url: "/data/spots",
		type: "GET",
		dataType: "json",
		success: function(result) {
			newSpots = result;
		}
	});

	// Loop through every spot, checking if its occupied.
	for(let i = 0; i < parking_spots.length; i++) {
		// If changes has occured between old and newly fetched,
		// set current spot to new spot.
		if(parking_spots[i].occupied != newSpots[i].occupied) {
			parking_spots[i].occupied = newSpots[i].occupied;
			updateSpot(parking_spots[i].type, parking_spots[i].number, parking_spots[i].occupied);
		}
	}
}

function updateSpot(type, number, occupied) {
	// Set targetTable to the value of HTML id's
	let targetTable;
	switch(type) {
		case "Guest":
			targetTable = table_guests;
      break;
		case "Student":
			targetTable = table_students;
      break;
		case "Staff":
			targetTable = table_staff;
      break;
	}

	let rowNumber;
	let columnNumber;

	// Figure out which row it is, as rows
	// have either even or odd spot numbers
	rowNumber = number % 2 == 0 ? 1 : 0;

	// Set columnNumber depending if its even or odd
	if(number % 2 == 0) {
		columnNumber = number / 2 - 1;
	} else {
		columnNumber = Math.floor(number / 2);
	}
	
	// Update the tables
	editSpotStatus(targetTable.rows[rowNumber].cells[columnNumber], occupied)
}

// Run the function ever .5 seconds
setInterval(function(){
	CheckSpots();
}, 500)

