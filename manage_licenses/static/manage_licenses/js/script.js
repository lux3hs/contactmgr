

// Load functions
window.addEventListener('load', (event) => {
  
  // Open default tab
  document.getElementById("js-default-open").click();

  // Load license table data
  loadTableData(url='get-license-data', tableID='license-table')
  
  document.getElementById("delete-license-button").addEventListener("click", function() {
    deleteTableData(url='delete-license-selection', tableID='license-table')
  
  })

  document.getElementById("license-search-button").addEventListener("click", function() {
    var choiceQuery = "license_search_form_choice_field"
    var searchQuery = "license_search_form_search_field"
    searchTableData(url='get-license-data', choiceQyery=choiceQuery, searchQuery=searchQuery, "license-table",)

  })

  document.getElementById("clear-license-search").addEventListener("click", function() {
    loadTableData(url='get-license-data', tableID='license-table')

  })


  
  // Load entitlement table data
  loadTableData(url='get-entitlement-data', tableID='entitlement-table')

  document.getElementById("entitlement-search-button").addEventListener("click", function() {
    var choiceQuery = "entitlement_search_form_choice_field"
    var searchQuery = "entitlement_search_form_search_field"
    searchTableData(url='get-entitlement-data', choiceQyery=choiceQuery, searchQuery=searchQuery, "entitlement-table",)
    
  })

  document.getElementById("clear-entitlement-search").addEventListener("click", function() {
    loadTableData(url='get-entitlement-data', tableID='entitlement-table')
  
  })
})
