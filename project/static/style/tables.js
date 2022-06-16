const maxRows = 2;
const maxColumns = 4;
const maxSpots = 8;

var table_guests = document.getElementById('parking-guests');
var table_staff = document.getElementById('parking-staff');
var table_students = document.getElementById('parking-students');

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

  function addTableCell(spot, row) {
    var td = row.insertCell();
    td.classList.add("park-spot");
    td.onclick = function () {
      tableCellClick(spot,td);
    }; 

         
    if(spot.occupied) {
      var imageAddress = "url('../static/style/Images/" + getRandomCarImage() + "')"
      td.style.backgroundImage = imageAddress; //"url('../static/style/Images/')";
    } else {
      td.style.backgroundImage = '';
    }
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
      freeStatus.innerHTML = "Taken";
    }
    else {
      freeStatus.innerHTML = "Free";
    }
  }

  function getRandomCarImage(){
    var rnd = Math.floor(Math.random() * 10) + 1;
    return 'car' + rnd + '.png';
  }


  // mainTable.rows[startCellY].cells[startCellX].classList.add('start-cell');
