// Transform the spots JSON variable into an array
let people = JSON.parse(peopleJson);

// Matches the account clicked with account list
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

// formats PostgreSQL datetime and returns only the date
function getDateOnly(dateString) {
    return dateString.substring(5, 16);
}

// Display account and parkbizz info in the info box
function displayAccountInfo(account, name, cpr) {
    document.querySelector("#infoBoxName h2").innerHTML = name;
    document.querySelector("#infoBoxCpr h2").innerHTML = cpr;
    document.querySelector("#infoBoxAccountNr h2").innerHTML = account.account_number;
    document.querySelector("#infoBoxBalance h2").innerHTML = account.balance;
    console.log(account.parkbizzes);
    account.parkbizzes.forEach(function(bizz) {
        document.querySelector("#infoBoxBizzSerial .bizz-serial").innerHTML += "<div><h2>" + bizz.serial_number + "</h2></div>";
        document.querySelector("#infoBoxExpiryDate .bizz-expiry-date").innerHTML += "<div><h2>" + getDateOnly(bizz.expiry_date) + "</h2></div>";
    })
}

// Populates the receipts table with receipts related to the account
function displayReceipts(receipts) {
    let table = document.querySelector("#receiptsTable tbody");
    table.innerHTML = '';
    receipts.forEach(function(receipt) {
        let row = table.insertRow()
        row.insertCell().innerHTML = receipt.receipt_id;
        row.insertCell().innerHTML = getDateOnly(receipt.entrance_time);
        row.insertCell().innerHTML = getDateOnly(receipt.exit_time);
        row.insertCell().innerHTML = receipt.total;
    })
}

// Receives reciepts related to account
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



 // Action to be performed by clicking on a account
 function clickAccount(accountNumber, name, cpr){
    let account = findAccount(accountNumber);

    if (account != undefined) {
        displayAccountInfo(account, name, cpr);
        let receipts = getReceipts(accountNumber);
    }
    else {
        console.log("No matching account")
    }

    let sideBox = document.querySelector("#sideBar");

    // Shows the info box if not already shown
    if (sideBox.classList == '') {
       sideBox.classList.add("shown");
       // Adds event listener to hide info box and hides the info box when clicking outside the
      document.querySelector("#tableContainer").addEventListener("click", function(e){
        if (!e.target.classList.contains("button-table") && sideBox.classList != '') {
          sideBox.classList.remove("shown");
          document.querySelector(".active").classList.remove("active"); 
        }
      })
    }
  }