

// Load functions
window.addEventListener('load', (event) => {

  // Open default tab
  document.getElementById("js-default-open").click();


    var contactTable = document.getElementById("contact-table");
    if (contactTable) {
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

    }



    var orgTable = document.getElementById("org-table");
    if (orgTable) {
      loadTableData(url='get-org-data', tableID='org-table')
  

    var productTable = document.getElementById("product-table");
    // console.log("hello")
    if (productTable) {
      loadTableData(url='get-product-data', tableID='product-table')
    }

    var entitlementTable = document.getElementById("entitlement-table");
    if (entitlementTable) {
      loadTableData(url='get-entitlement-data', tableID='entitlement-table')
    }

  }
})
