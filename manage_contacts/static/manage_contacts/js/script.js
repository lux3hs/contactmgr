

// Load functions
window.addEventListener('load', (event) => {

  // Open default tab
  document.getElementById("js-default-open").click();



  // var orgTable = document.getElementById("org-table");
  // if(orgTable) {
  //   var fetchData = fetchRequest(url='get-org-data');

  //   fetchData.then(data => {
  //     tableHeader = data.table_header
  //     tableData = data.table_data
  //     buildDataTable(tableData, tableHeader, 'org-table')
  //     addCheckBoxes('org-table')
  //     })
  // }


  // Load contact table data
  loadTableData(url='get-contact-data', tableID='contact-table')

    document.getElementById("delete-contact-button").addEventListener("click", function() {
      deleteTableData(url='delete-contact-selection', tableID='contact-table')
    
    })

    document.getElementById("contact-search-button").addEventListener("click", function() {
      var choiceQuery = "contact_search_form_choice_field";
      var searchQuery = "contact_search_form_search_field";
      searchTableData(url='get-contact-data', choiceQyery=choiceQuery, searchQuery=searchQuery, "contact-table",)

    })

  document.getElementById("clear-contact-search").addEventListener("click", function() {
    loadTableData(url='get-contact-data', tableID='contact-table')

    })
  })
