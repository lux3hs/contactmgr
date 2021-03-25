

// Load functions
window.addEventListener('load', (event) => {




  // Open default tab
  document.getElementById("js-default-open").click();

  // Load license table data
  // var licenseTable = document.getElementById("license-table");
  // if (licenseTable) {
  loadTableData(url='get-license-data', tableID='license-table')
  // }

  // Load entitlement table data
  loadTableData(url='get-entitlement-data', tableID='entitlement-table')

  // Check for delete button press
  document.getElementById("delete-license-button").addEventListener("click", function() {
    deleteTableData(url='delete-license-selection', tableID='license-table');

  })

})

  
  
  
  
  
  
  


      




                //  url1='generate-license-selection/187'
                          //  url2='generate-license-selection/187'



                              // Promise.all([fetch(url1),fetch(url2)
                              // ])
                              // .then(result => {
                              //   nodeList = result
                              //   for (i = 0; i <	nodeList.length; i++) {
                              //     console.log(result[i])

                            

                              //   for (i = 0; i <	nodeList.length; i++) {
                              //     console.log(result[i])

                              //   }            
                                
                              // }
                              
                              // })



  // document.getElementById("license-search-button").addEventListener("click", function() {
  //   var choiceQuery = "license_search_form_choice_field"
  //   var searchQuery = "license_search_form_search_field"
  //   searchTableData(url='get-license-data', choiceQyery=choiceQuery, searchQuery=searchQuery, "license-table",)

  // })

  // document.getElementById("clear-license-search").addEventListener("click", function() {
  //   loadTableData(url='get-license-data', tableID='license-table')

  // })


  

  // document.getElementById("entitlement-search-button").addEventListener("click", function() {
  //   var choiceQuery = "entitlement_search_form_choice_field"
  //   var searchQuery = "entitlement_search_form_search_field"
  //   searchTableData(url='get-entitlement-data', choiceQyery=choiceQuery, searchQuery=searchQuery, "entitlement-table",)
    
  // })

  // document.getElementById("clear-entitlement-search").addEventListener("click", function() {
  //   loadTableData(url='get-entitlement-data', tableID='entitlement-table')
  
  // })




// Simple timer

 // var myVar;

          // function myFunction() {
          //   myVar = setTimeout(alertFunc, 001);
          // }
          
          // function alertFunc() {
          //   loadTableData(url='get-license-data', tableID='license-table')
          // }
          
          // myFunction()







      // licenseSelection = [187, 189]

      // url='generate-license-selection'

      // string = 'download-license-package/' + licenseSelection

      // data = JSON.stringify(string)

  

  //   window.addEventListener('load', (event) => {

  // var licenseTable = document.getElementById("license-table");


  // if (licenseTable) {
  //   console.log('hello')


  // document.getElementById("download-license-button").addEventListener("click", (event) => {

    
       
    
  //   license_list = [187, 189]
  //       //  array = {'values':license_list}
  //       array = license_list

  //        info = JSON.stringify(array)

  //     url = 'download-license-package/' + info





      // var download = browswer.downloads.download({

      //   url : url,
      //   filename : 'myfile.lic',
      //   conflictAction : 'uniquify'

      // })

      // console.log(download)





//       var csrfToken =  document.getElementsByName('csrfmiddlewaretoken')[0].value;

//       fetch(url, {
//           method: 'GET',
//       })

//       .then(data => {return data})
//       .then(response => {

//           console.log(response);
//       })

//     })
//   }

// })