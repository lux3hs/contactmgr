

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
    loadTableData(url='get-contact-data', tableID='contact-table')

    document.getElementById("delete-contact-button").addEventListener("click", function() {
      deleteTableData(url='delete-contact-selection', tableID='contact-table')
      
    })

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

      document.getElementById("delete-org-button").addEventListener("click", function() {
        deleteTableData(url='delete-org-selection', tableID='org-table')
      })



      document.getElementById("org-search-button").addEventListener("click", function() {
        var choiceQuery = "org_search_form_choice_field";
        var searchQuery = "org_search_form_search_field";
        searchTableData(url='get-org-data', choiceQyery=choiceQuery, searchQuery=searchQuery, "org-table")
  
      })
  
      document.getElementById("clear-org-search").addEventListener("click", function() {
        loadTableData(url='get-org-data', tableID='org-table')
  
        })
    
    }


    // Load product table data
    var productTable = document.getElementById("product-table");
    if (productTable) {
      loadTableData(url='get-product-data', tableID='product-table')
    
      document.getElementById("delete-product-button").addEventListener("click", function() {
        deleteTableData(url='delete-product-selection', tableID='product-table')
      })


      document.getElementById("product-search-button").addEventListener("click", function() {
        var choiceQuery = "product_search_form_choice_field";
        var searchQuery = "product_search_form_search_field";
        searchTableData(url='get-product-data', choiceQyery=choiceQuery, searchQuery=searchQuery, "product-table")
  
      })
  
      document.getElementById("clear-product-search").addEventListener("click", function() {
        loadTableData(url='get-product-data', tableID='product-table')
  
        })
  
    }





// Modals

// Contact Form
var contactModal = document.getElementById("add-contact-modal");
var contactButton = document.getElementById("add-contact-button");
var contactSpan = document.getElementsByClassName("close-contact-form")[0];

contactButton.onclick = function() {
  contactModal.style.display = "block";
}

contactSpan.onclick = function() {
  contactModal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == contactModal) {
    contactModal.style.display = "none";
  }
} 


// Org Form
var orgModal = document.getElementById("add-org-modal");
var orgButton = document.getElementById("add-org-button");
var orgSpan = document.getElementsByClassName("close-org-form")[0];

orgButton.onclick = function() {
  orgModal.style.display = "block";
}

orgSpan.onclick = function() {
  orgModal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == orgModal) {
    orgModal.style.display = "none";
  }
} 



// Product Form
var productModal = document.getElementById("add-product-modal");
var productButton = document.getElementById("add-product-button");
var productSpan = document.getElementsByClassName("close-product-form")[0];

productButton.onclick = function() {
  productModal.style.display = "block";
}

productSpan.onclick = function() {
  productModal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == productModal) {
    productModal.style.display = "none";
  }
} 



})



