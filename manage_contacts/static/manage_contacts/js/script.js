

window.addEventListener('load', (event) => {
  document.getElementById("js-default-open").click();

  var fetchData = fetchRequest(url='get-contact-data');
  fetchData.then(data => {
    tableHeader = data.table_header
    tableData = data.table_data
    buildDataTable(tableData, tableHeader, 'contact-table')
    addCheckBoxes('contact-table')
    })

  document.getElementById("contact-search-button").addEventListener("click", function() {
    var choiceQuery = document.getElementById("contact_search_form_choice_field").value;
    var searchQuery = document.getElementById("contact_search_form_search_field").value;
    fetchData.then(data => {
    tableData = data.table_data
    tableHeader = data.table_header
    filteredData = filterData(tableData, choiceQuery, searchQuery);
    buildDataTable(filteredData, tableHeader, 'contact-table')
    addCheckBoxes('contact-table')
    })
  })

 document.getElementById("clear-contact-search").addEventListener("click", function() {
    fetchData.then(data => {
    tableData = data.table_data
    tableHeader = data.table_header
    buildDataTable(tableData, tableHeader, 'contact-table')
    addCheckBoxes('contact-table')
    })
  })
})