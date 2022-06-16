// Transform the spots JSON variable into an array
let people = JSON.parse(peopleJson);


function findAccount(accountNumber) {
    let matchedAccount = undefined;
    people.forEach(function(person) {
        person.accounts.forEach(function(account){
            if(account.account_number == accountNumber) {
                matchedAccount = account;
            }
        })
    })
    return matchedAccount;
}



function displayAccountInfo(account, name, cpr) {
    document.querySelector("#infoBoxName h2").innerHTML = name;
    document.querySelector("#infoBoxCpr h2").innerHTML = cpr;
    document.querySelector("#infoBoxAccountNr h2").innerHTML = account.account_number;
    document.querySelector("#infoBoxBalance h2").innerHTML = account.balance;
    document.querySelector("#infoBoxBizzSerial h2").innerHTML = account.parkbizzes[0].serial_number;
    document.querySelector("#infoBoxExpiryDate h2").innerHTML =  account.parkbizzes[0].expiry_date;
}

function displayReceipts(receipts) {
    let table = document.querySelector("#receiptsTable");
    receipts.forEach(function(receipt) {
        let row = table.insertRow()
    })
    console.log(receipts);
}

function getReceipts(account_number) {
    let receipts;
    $.ajax({
		url: "/data/receipts",
		type: "GET",
        data: {"account_number": account_number},
        contentType: "application/json",
		dataType: "json",
		success: function(result) {
			receipts = result;
            displayReceipts(receipts);
		}
	});

    return receipts;
}



 // Action to be performed by clicking on a parking spot
 function clickAccount(accountNumber, name, cpr){
    let account = findAccount(accountNumber);
    if (account != undefined) {
        displayAccountInfo(account, name, cpr);
        let receipts = getReceipts(accountNumber);
    }
    else {
        console.log("Account not matched")
    }

    // Finds the previous active spot if any
    let sideBox = document.querySelector("#sideBar");

    // Shows the info box if not already shown
    if (sideBox.classList == '') {
       sideBox.classList.add("shown");
       // Adds event listener to hide info box and remove active spot when not clicking on spots
      document.querySelector("#tableContainer").addEventListener("click", function(e){
        if (!e.target.classList.contains("button-table") && sideBox.classList != '') {
          sideBox.classList.remove("shown");
          document.querySelector(".active").classList.remove("active"); 
        }
      })
    }
  }