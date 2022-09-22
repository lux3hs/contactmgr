

// Load functions
window.addEventListener('load', (event) => {

  
  // Open default tab
  var jsDefaultOpen = document.getElementById("js-default-open")
  if (jsDefaultOpen) {
  document.getElementById("js-default-open").click();
  }

  // Load contact table data
  var contactTable = document.getElementById("contact-table");
  if (contactTable) {

    loadTableData(url='get-contact-data', tableID='contact-table', tableChecks=true)


    // document.getElementById("delete-contact-button").addEventListener("click", function() {

    //   deleteTableData(url='delete-contact-selection', tableID='contact-table')
    
    // })

    document.getElementById("contact-search-button").addEventListener("click", function() {
      var choiceQuery = "contact_search_form_choice_field";
      var searchQuery = "contact_search_form_search_field";
      searchTableData(url='get-contact-data', choiceQyery=choiceQuery, searchQuery=searchQuery, "contact-table")

    })

    document.getElementById("clear-contact-search").addEventListener("click", function() {
      loadTableData(url='get-contact-data', tableID='contact-table')

      })
  }


  // Load org table data
  var orgTable = document.getElementById("org-table");
  if (orgTable) {
      loadTableData(url='get-org-data', tableID='org-table')

      // document.getElementById("delete-org-button").addEventListener("click", function() {
      //   deleteTableData(url='delete-org-selection', tableID='org-table')
      // })
    
    }


    // Load product table data
    var productTable = document.getElementById("product-table");
    if (productTable) {
      loadTableData(url='get-product-data', tableID='product-table')
    
      document.getElementById("delete-product-button").addEventListener("click", function() {
        deleteTableData(url='delete-product-selection', tableID='product-table')
      })
  
    }


    // // Load entitlement table data
    var entitlementTable = document.getElementById("entitlement-table");
    if (entitlementTable) {
      loadTableData(url='get-entitlement-data', tableID='entitlement-table')

      // document.getElementById("delete-entitlement-button").addEventListener("click", function() {
      //   var queryData = getCheckboxValues('js-check-box')
      //   deleteTableData(url='delete-entitlement-selection', queryData=queryData, tableID='entitlement-table')

      // })

    }

})

