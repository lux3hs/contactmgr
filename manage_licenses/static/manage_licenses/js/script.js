

window.addEventListener('load', (event) => {
  document.getElementById("js-default-open").click();

  var fetchData = fetchRequest(url='get-license-data');
  fetchData.then(data => {
    tableHeader = data.table_header
    tableData = data.table_data
    buildDataTable(tableData, tableHeader, 'license-table')
    addCheckBoxes('license-table')
    })


    document.getElementById("license-search-button").addEventListener("click", function() {
      var choiceQuery = document.getElementById("license_search_form_choice_field").value;
      var searchQuery = document.getElementById("license_search_form_search_field").value;
      fetchData.then(data => {
      tableData = data.table_data
      tableHeader = data.table_header
      filteredData = filterData(tableData, choiceQuery, searchQuery);
      buildDataTable(filteredData, tableHeader, 'license-table')
      addCheckBoxes('license-table')
      })
    })

    document.getElementById("clear-license-search").addEventListener("click", function() {
      fetchData.then(data => {
      tableData = data.table_data
      tableHeader = data.table_header
      buildDataTable(tableData, tableHeader, 'license-table')
      addCheckBoxes('license-table')
      })
  })



  var fetchData = fetchRequest(url='get-entitlement-data');
  fetchData.then(data => {
    tableHeader = data.table_header
    tableData = data.table_data
    buildDataTable(tableData, tableHeader, 'entitlement-table')
    })


  document.getElementById("entitlement-search-button").addEventListener("click", function() {
    var choiceQuery = document.getElementById("entitlement_search_form_choice_field").value;
    var searchQuery = document.getElementById("entitlement_search_form_search_field").value;
    fetchData.then(data => {
    tableData = data.table_data
    tableHeader = data.table_header
    filteredData = filterData(tableData, choiceQuery, searchQuery);
    buildDataTable(filteredData, tableHeader, 'entitlement-table')
    })
  })

  document.getElementById("clear-entitlement-search").addEventListener("click", function() {
    fetchData.then(data => {
    tableData = data.table_data
    tableHeader = data.table_header
    buildDataTable(tableData, tableHeader, 'entitlement-table')
    })
  })
})
