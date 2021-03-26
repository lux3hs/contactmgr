
// Change page tabs
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



  // Collect data from a url
  function fetchRequest(url) {
    return fetch(url)
    .then(response => { return response.json()})
    .catch(error => console.log('error:', error))
  }
  
  // Filter collected data
  function filterData(data, key, value) {
    var tableData = data
    var keyQuery = key;
    let valueQuery = String(value).toLowerCase();
    var filteredValues = [];
    var dataFilter = []
    for (let element of tableData) {
      let keys = Object.keys(element)
  
      for (key of keys) {
        if (String(key) == keyQuery) {
          filteredValues.push(element[key]);
          console.log("values: " + filteredValues)
  
          for (value of filteredValues) {
            cleanValue = String(value).toLowerCase()
            if (cleanValue.includes(valueQuery)) {
              dataFilter.push(element);
              var filteredValues = [];
              break
            }
         }        
       }
     }
   }
    return dataFilter
  }

  // Build a data table out of collected data
  function buildDataTable(tableData, tableHeader, tableID) {
    let headerData=tableHeader;
    let data = tableData;
    const table = document.getElementById(tableID);
    table.innerHTML = "";
    const header = table.createTHead();
    const row = header.insertRow(0);
    for(let value in headerData) {  
      const cell = row.insertCell(-1);
      cell.outerHTML = "<th>" + headerData[value] + "</th>";
    }

    if(!data) {
      console.log("table object doesn't exist")
      return
    }

    for(let dataObject of data) {
      const data_id = dataObject.data_id
      delete dataObject.data_id
      const drow = table.insertRow(-1);
  
      dataKeys = Object.keys(dataObject);
      drow.setAttribute("id", data_id)
  
      for(let dataKey of dataKeys) {      
        dataValue = dataObject[dataKey];
        drow.insertCell(-1).innerHTML = dataValue;
      }
    }
  }
  


  // Add checkboxes to tables (Switch to widgets)
  function addCheckBoxes(tableID) {
    var x = document.getElementById(tableID).rows.length;
    var table = document.getElementById(tableID);
    var num = table.rows;
  
    for (i in num){
      let row = table.rows[i]
      if (i == 0){
        x = document.getElementById(tableID).rows[0]
        cell = x.insertCell(0)
        cell.outerHTML = "<th></th>"; 
  
      }
  
      else if(!isNaN(i)) {
        let row = document.getElementById(tableID).rows[i]
        let cell = row.insertCell(0)
        var tableRow = document.getElementById(tableID).getElementsByTagName("tr");
        var rowID = tableRow[i].id
  
        var x = document.createElement("INPUT");
        x.setAttribute("type", "checkbox");
        x.setAttribute("name", "check-box")
        x.setAttribute("class", "checkBox")
        x.setAttribute("value", rowID);
        cell.appendChild(x);
  
      }
    }
  }


  // Get values from checkboxes
  function getCheckboxValues() {
    
    var nodeList = document.getElementsByName("check-box");
    checkBoxValues = []
    for (i = 0; i <	nodeList.length; i++) {
      checked = nodeList[i].checked;
      value = nodeList[i].value;
     
      if (checked == true) {
        checkBoxValues.push(value)
      }
    }

    return checkBoxValues
  }



  // Dynamic table processing

  // Build a table on page load
  function loadTableData(url, tableID) {
    var fetchData = fetchRequest(url);
    fetchData.then(data => {
      tableHeader = data.table_header
      tableData = data.table_data
      buildDataTable(tableData, tableHeader, tableID)
      addCheckBoxes(tableID)

    })
  }


  // Delete data from a table and rebuild
  function deleteTableData(url, tableID) {      
    queryData = getCheckboxValues()
    query_string = JSON.stringify(queryData)
        requestURL = url + '/' + query_string     
        newRequest = fetchRequest(requestURL)
        newRequest.then(data => {
          tableData = data.table_data
          tableHeader = data.table_header
          buildDataTable(tableData, tableHeader, tableID)
          addCheckBoxes(tableID)
                 
        })
  }

  // Search data within a table and rebuild
  function searchTableData(url, choiceQuery, searchQuery, tableID) {
      var fetchData = fetchRequest(url);
      var choice = document.getElementById(choiceQuery).value;
      var search = document.getElementById(searchQuery).value;
      
      fetchData.then(data => {
        tableData = data.table_data
        tableHeader = data.table_header
        filteredData = filterData(tableData, choice, search);
        buildDataTable(filteredData, tableHeader, tableID);

        addCheckBoxes(tableID)

      })
  }