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
    td.onclick = function () {
      tableCellClick(spot);
    }; 

         
    if(spot.occupied) {
      var imageAddress = "url('../static/style/Images/" + getRandomCarImage() + "')"
      td.style.backgroundImage = imageAddress; //"url('../static/style/Images/')";
    } else {
      td.style.backgroundImage = '';
    }
  }

  function tableCellClick(spot){
    console.log(spot);
  }

  function getRandomCarImage(){
    var rnd = Math.floor(Math.random() * 10) + 1;
    return 'car' + rnd + '.png';
  }


  // mainTable.rows[startCellY].cells[startCellX].classList.add('start-cell');
