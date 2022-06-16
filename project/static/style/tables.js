const maxRows = 2;
const maxColumns = 4;
const maxSpots = 8;

var table_guests = document.getElementById('parking-guests');
var table_staff = document.getElementById('parking-staff');
var table_students = document.getElementById('parking-students');

let checking = false;

// Transform the spots JSON variable into an array
var parking_spots = JSON.parse(spots);


tableCreate(table_staff, 'Staff');
tableCreate(table_students, 'Student');
tableCreate(table_guests, 'Guest');

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

    if (prevActive != undefined) {
      prevActive.classList.remove("active");
    }
    else {
      // Adds event listener to hide info box and remove active spot when not clicking on spots
      document.querySelector("#parkingLot").addEventListener("click", function(e){
        if (!e.target.classList.contains("park-spot")) {
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
      freeStatus.data = "Taken";
    }
    else {
      freeStatus.data = "Free";
    }
  }

  function getRandomCarImage(){
    var rnd = Math.floor(Math.random() * 10) + 1;
    return 'car' + rnd + '.png';
  }


// Cchecking for updates between database and existing spots
let newSpots;

function CheckSpots() {
	$.ajax({
		url: "/data/spots",
		type: "GET",
		dataType: "json",
		success: function(result) {
			newSpots = result;
		}
	});

	for(let i = 0; i < parking_spots.length; i++) {
		if(parking_spots[i].occupied != newSpots[i].occupied) {
			parking_spots[i].occupied = newSpots[i].occupied;
			updateSpot(parking_spots[i].type, parking_spots[i].number, parking_spots[i].occupied);
		}
	}
}

function updateSpot(type, number, occupied) {
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

	rowNumber = number % 2 == 0 ? 1 : 0;
	
	if(number % 2 == 0) {
		columnNumber = number / 2 - 1;
	} else {
		columnNumber = Math.floor(number / 2);
	}
	
	editSpotStatus(targetTable.rows[rowNumber].cells[columnNumber], occupied)

}

setInterval(function(){
	CheckSpots();
}, 1000)
