// Transform the spots JSON variable into an array
let people = JSON.parse(peopleJson);

console.log(people)

function findAccount(accountNumber) {
    let matchedAccount = undefined;
    people.forEach(function(person) {
        person.accounts.forEach(function(account){
            console.log(accountNumber + " : " + account.account_number)
            if(account.account_number == accountNumber) {
                console.log(account);
                matchedAccount = account;
            }
        })
    })
    return matchedAccount;
}



function displayAccountInfo(account, name, cpr) {
    console.log(account);
    document.querySelector("#infoBoxName h2").innerHTML = name;
    document.querySelector("#infoBoxCpr h2").innerHTML = cpr;
    document.querySelector("#infoBoxAccountNr h2").innerHTML = account.account_number;
    document.querySelector("#infoBoxBalance h2").innerHTML = account.balance;
    document.querySelector("#infoBoxBizzSerial h2").innerHTML = account.parkbizzes[0].serial_number;
    document.querySelector("#infoBoxExpiryDate h2").innerHTML =  account.parkbizzes[0].expiry_date;
}

 // Action to be performed by clicking on a parking spot
 function clickAccount(accountNumber, name, cpr){
    let account = findAccount(accountNumber);
    if (account != undefined) {
        displayAccountInfo(account, name, cpr);
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
      document.querySelector("#parkingLot").addEventListener("click", function(e){
        if (!e.target.classList.contains("button-table")) {
          sideBox.classList.remove("shown");
          document.querySelector(".active").classList.remove("active"); 
        }
      })
    }
  }