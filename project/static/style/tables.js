const maxRows = 2;
const maxColumns = 4;

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

  var tr1 = table.insertRow();  
  var tr2 = table.insertRow();

  var td1_0 = tr1.insertCell();

  td1_0.onclick = function () {
            tableCellClick(sortedArray[0]);
        };        


  var td1_1 = tr1.insertCell();

  td1_1.onclick = function () {
    tableCellClick(sortedArray[1]);
         };

  if(!sortedArray[0].occupied) {
    td1_0.classList.add('spot-free');
  } else {
    td1_1.classList.add('spot-taken');
  }
  



  var td1_2 = tr1.insertCell();

  var td1_3 = tr1.insertCell();

  var td2_0 = tr2.insertCell();
  var td2_1 = tr2.insertCell();
  var td2_2 = tr2.insertCell();
  var td2_3 = tr2.insertCell();

  // for(var i = 0; i < maxRows; i++){

      // var tr1 = mainTable.insertRow();
      // var tr2 = mainTable.insertRow();

 

      // for(var j = 0; j < maxColumns; j++){
      //     var td = tr.insertCell();
      //     td.xPos = j;
      //     td.yPos = i;
      //     td.stype = spots
      //     td.visited = false;

      //     td.onclick = function () {
      //         tableCellClick(this);
      //     };



      //     // td.addEventListener('mousemove', function () {
      //     //     tableCellMouseMove(this);
      //     // })

      //     // td.addEventListener('mouseclick', function () {
      //     //     tableCellClick(this);
      //     // })

      //     td.classList.add('empty-cell');
      //     //td.onclick
      //     //td.addEventListener("click", tableCellClick(this), false);


      // }
  }

  function tableCellClick(spot){
    console.log(spot);
  }


  // mainTable.rows[startCellY].cells[startCellX].classList.add('start-cell');
