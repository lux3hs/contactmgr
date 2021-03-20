
// Page tab functions
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


// Filter table data based on search query
function filterTableData(tableData, filterQuery) {  
  var filteredData = [];
  var tableData = tableData
  var filterQuery = filterQuery
  for(let element of tableData) {
    keys = Object.keys(element)
    for (key of keys) {          
      if (String(element[key]).includes(filterQuery)) {
        filteredData.push(element);
        break
      }
    }
  }

  return filteredData
}

// Build table based on data
function buildTable(url, tableID, filterQuery="", checkWidget=false) {
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

  let headerData=data.table_header;
  const table = document.getElementById(tableID);
  table.innerHTML = "";
  const header = table.createTHead();
  const row = header.insertRow(0);
  for(let value in headerData) {  
    const cell = row.insertCell(-1);
    cell.outerHTML = "<th>" + headerData[value] + "</th>";
  }

  if (data.success == true) {
    let tableData = data.table_data;
    if (filterQuery.length > 0) {
      tableData = filterTableData(tableData, filterQuery);
    }

    for(let dataObject of tableData) {

      const data_id = dataObject.data_id

      delete dataObject.data_id
      const drow = table.insertRow(-1);
      dataKeys = Object.keys(dataObject);
      // console.log(dataObject.data_id)
      
      drow.setAttribute("id", data_id)


      for(let dataKey of dataKeys) {      
        dataValue = dataObject[dataKey];
        drow.insertCell(-1).innerHTML = dataValue;
      }
    }
     
    console.log(checkWidget)
    if (checkWidget == true) {
    addCheckBoxes(tableID);

    }

  } 
      
  else {
      console.log("error")
    }
 
  })
}

function addCheckBoxes(tableID) {
  var x = document.getElementById(tableID).rows.length;

  // console.log(tableID)
  var table = document.getElementById(tableID);
  // var tableCell = document.getElementById(tableID).rows[1].cells;
  var num = table.rows;

  for (i in num){
    let row = table.rows[i]
    if (i == 0){
      // console.log("header")
      // console.log(i)
      x = document.getElementById(tableID).rows[0]

      cell = x.insertCell(0)

      // var x = document.createElement("INPUT");
      // x.setAttribute("type", "checkbox");
      // x.setAttribute("value", "")
      // x.setAttribute("id", 'checkBox');
      // cell.appendChild(x);
      cell.outerHTML = "<th></th>"; 

    }

    else if(!isNaN(i)) {
      // console.log("cell")
      // console.log(i)
      let row = document.getElementById(tableID).rows[i]
      let cell = row.insertCell(0)

      var tableRow = document.getElementById(tableID).getElementsByTagName("tr");
      var rowID = tableRow[i].id

      var x = document.createElement("INPUT");
      x.setAttribute("type", "checkbox");
      x.setAttribute("name", "check-box")
      x.setAttribute("value", rowID);
      cell.appendChild(x);

    }
  }

}


window.addEventListener('load', (event) => {

  document.getElementById("js-default-open").click();

  buildTable(url="get-license-data", tableID="license-table", filterQuery='', checkWidget=true);
  // addCheckBoxes('license-table');
  buildTable("get-entitlement-data", "entitlement-table");

  document.getElementById("license-search-button").addEventListener("click", function() {
  var filterQuery = document.getElementById("license-search-form").value;
  buildTable(url="get-license-data", tableID="license-table", filterQuery=filterQuery, checkWidget=true);
  })

  document.getElementById("clear-license-search").addEventListener("click", function(){
    buildTable(url="get-license-data", tableID="license-table", filterQuery='', checkWidget=true);
  })

  document.getElementById("delete-license-button").addEventListener("click", function() {
    var table = document.getElementById("license-table");
  })

  document.getElementById("entitlement-search-button").addEventListener("click", function() {
    console.log("hello")
    var filterQuery = document.getElementById("entitlement-search-form").value;
    buildTable("get-entitlement-data", "entitlement-table", filterQuery);    
  })

  document.getElementById("clear-entitlement-search").addEventListener("click", function(){
    buildTable("get-entitlement-data", "entitlement-table");
  })
})
