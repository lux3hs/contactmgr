function changePage(evt, pageName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("js-tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("js-tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(pageName).style.display = "block";
  evt.currentTarget.className += " active";

}

// function testFunction() {
//   document.getElementById("table1").innerHTML = "Hello!";
//   console.log("hellothere!!!");
//   var field = getElementById("id_search_query")
//   console.log(field)
// }


// Set basic form inputs

var formID = "search-form";
var fieldID = "id_search_query";

// Get value from submitted form for search query
function getFormValue(formID, fieldID) {
  form = document.getElementById(formID);
  value = form.elements.namedItem(fieldID).value;
  
  return value
}

// Filter table data based on search query
function filterTableData(tableData, filterQuery) {
  var filteredTableData = [];
  for(let element of tableData) {
    keys = Object.keys(element);
    for (key of keys) {
        if (element[key].includes(filterQuery)) {
          filteredTableData.push(element);
          break
        }
    }
  }

  return filteredTableData
}

// Build table based on filtered data
function buildTable(url, tableID) {
fetch(url, {
  headers:{
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
  },
 })

 .then(response => {
  return response.json() //Convert response to JSON
 })

 .then(data => { //Perform actions with the response data from the view
  const table = document.getElementById(tableID);
  

  
  if (data.success == true) {
    let tableData = data.table_data;
    let formValue = getFormValue(formID, fieldID)
    let filteredData = filterTableData(tableData, formValue)
      
    table.innerHTML = "";
    const header = table.createTHead();
    const row = header.insertRow(0);

    if (filteredData.length > 0) {
      tempObject = filteredData[0];
      tempKeys = Object.keys(tempObject);
      for(let value in tempKeys) {
        const cell = row.insertCell(-1);
        cell.outerHTML = "<th>" + tempKeys[value] + "</th>";
        }
    }
    for(let dataObject of filteredData) {
      const drow = table.insertRow(-1);
      dataKeys = Object.keys(dataObject);
      
      for(let dataKey of dataKeys) {      
        dataValue = dataObject[dataKey];
        drow.insertCell(-1).innerHTML = dataValue;

      }
    }
  } else{
    console.log("error")
  }
 })
}



// window.onload = function() {
//   var currentLocation = window.location.href;
//   testFetch(currentLocation);
// };