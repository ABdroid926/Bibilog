# Bibilog
A python based library system designed for easy adaptation. 
Bibilog runs with streamlit,google apps script(a gsheet extension )

1. How do I start my very own Bibilog?

Glad you've asked that mate! 

STEP 1 : 
Create a gsheet inventory of the library MAKING SURE that :

 - there are two tabs, names "Books" & "Users"
 - under "Books" make sure that there are "id","title","borrowed_by","due_date","status"(going from A1-E1)
 - under "Users" make sure that there are "username","password","isAdmin"(from A1 - C1)
 - make sure that all values under id is an int value and all values under "isAdmin" a boolean one

STEP 2 : 
Add this javascript code to google apps script (available under "extensions") : 

 <details>
    <summary> Google Apps Script function(white-coded) </summary>

``` javascript   
var ss = SpreadsheetApp.getActiveSpreadsheet();
var userSheet = ss.getSheetByName("Users");
var bookSheet = ss.getSheetByName("Books");


function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var action = String(data.action).trim().toLowerCase();
   
    // 1. LOGIN ACTION
    if (action === "login") {
      var username = data.username;
      var password = data.password;
      
      var rows = userSheet.getDataRange().getValues();
      for (var i = 1; i < rows.length; i++) {
        if (String(rows[i][0]).trim() === String(username).trim() && String(rows[i][1]).trim() === String(password).trim()) {
          var isAdmin = String(rows[i][2]).trim().toUpperCase(); 
          if (isAdmin === "TRUE") {
            return ContentService.createTextOutput("Admin Success");
          } else {
            return ContentService.createTextOutput("Success");
          }
        }
      }
      return ContentService.createTextOutput("Failure");
    }
    
    // 2. SIGNUP ACTION (Supports "register" or "signup")
    else if (action === "register" || action === "signup") {
      var username = data.username;
      var password = data.password;
      
      var rows = userSheet.getDataRange().getValues();
      for (var i = 1; i < rows.length; i++) {
        if (String(rows[i][0]).trim() === String(username).trim()) {
          return ContentService.createTextOutput("User Exists");
        }
      }
      
      userSheet.appendRow([username, password, "FALSE"]);
      return ContentService.createTextOutput("Success");
    }
    
    // 3. ISSUE BOOK ACTION (Supports "borrowed_by" and "due_date")
    else if (action === "issue_book") {
      var rawBookID = data.bookID !== undefined ? data.bookID : (data.id !== undefined ? data.id : data.book_id);
      var bookID = String(rawBookID).trim();
      
      var username = data.borrowed_by !== undefined ? data.borrowed_by : data.username;
      var rawLoan = data.due_date !== undefined ? data.due_date : data.loan_period;
      var loanPeriod = parseInt(rawLoan);
      if (isNaN(loanPeriod)) { loanPeriod = 7; }
      
      var dueDate = new Date();
      dueDate.setDate(dueDate.getDate() + loanPeriod);
      var formattedDueDate = Utilities.formatDate(dueDate, Session.getScriptTimeZone(), "yyyy-MM-dd");
      
      var rows = bookSheet.getDataRange().getValues();
      for (var i = 1; i < rows.length; i++) {
        var sheetVal = rows[i][0];
        var sheetBookID = String(sheetVal).trim();
        
        if (sheetBookID === bookID || parseFloat(sheetBookID) === parseFloat(bookID)) {
          bookSheet.getRange(i + 1, 3).setValue(username);          // Column C: Username
          bookSheet.getRange(i + 1, 4).setValue(formattedDueDate);  // Column D: Due Date
          bookSheet.getRange(i + 1, 5).setValue("Active");          // Column E: Status
          
          return ContentService.createTextOutput("Success");
        }
      }
      return ContentService.createTextOutput("Book Not Found");
    }
    
    // 4. GET USER BOOKS ACTION
    else if (action === "get_user_books") {
      var username = data.username;
      var rows = bookSheet.getDataRange().getValues();
      var userBooks = [];
      
      for (var i = 1; i < rows.length; i++) {
        var borrowedBy = String(rows[i][2]).trim();
        if (borrowedBy === String(username).trim()) {
          userBooks.push({
            bookID: rows[i][0],
            title: rows[i][1],
            dueDate: rows[i][3],
            status: rows[i][4]
          });
        }
      }
      
      var output = ContentService.createTextOutput(JSON.stringify(userBooks));
      output.setMimeType(ContentService.MimeType.JSON);
      return output;
    }

    // 5. GET ALL LOANS ACTION (For Admin Active Loans Section)
    else if (action === "get_all_loans") {
      var rows = bookSheet.getDataRange().getValues();
      var allLoans = [];
      
      for (var i = 1; i < rows.length; i++) {
        var status = String(rows[i][4]).trim();
        // Grabs books that are currently checked out/active
        if (status !== "" && status.toLowerCase() !== "available" && status.toLowerCase() !== "returned") {
          allLoans.push({
            bookID: rows[i][0],
            title: rows[i][1],
            borrowedBy: rows[i][2],
            dueDate: rows[i][3],
            status: status
          });
        }
      }
      
      var output = ContentService.createTextOutput(JSON.stringify(allLoans));
      output.setMimeType(ContentService.MimeType.JSON);
      return output;
    }

    // 6. RETURN BOOK ACTION (For Admin Mark Return Button)
    else if (action === "return_book") {
      var rawBookID = data.bookID !== undefined ? data.bookID : (data.id !== undefined ? data.id : data.book_id);
      var bookID = String(rawBookID).trim();
      
      var rows = bookSheet.getDataRange().getValues();
      for (var i = 1; i < rows.length; i++) {
        var sheetVal = rows[i][0];
        var sheetBookID = String(sheetVal).trim();
        
        if (sheetBookID === bookID || parseFloat(sheetBookID) === parseFloat(bookID)) {
          bookSheet.getRange(i + 1, 3).setValue("");        // Clear Username
          bookSheet.getRange(i + 1, 4).setValue("");        // Clear Due Date
          bookSheet.getRange(i + 1, 5).setValue("Available"); // Reset Status
          
          return ContentService.createTextOutput("Success");
        }
      }
      return ContentService.createTextOutput("Book Not Found");
    }
    
    return ContentService.createTextOutput("Invalid Action: " + action);
    
  } catch (err) {
    return ContentService.createTextOutput("Script Error: " + err.toString());
  }
}
```
</details> 

STEP 3 : dont worry,this is the last set.

- Make sure you own a streamlit account 
- Add the gsheet link to streamlit secrets as "SHEET_URL"
- fork app.py , .github/workflows & .streamlit to your own account
- deploy it on streamlit!

 NOTE : Bibilog was made as a part of a school project, however you are free to use,modify or share Bibilog for any personal and non-commercial usage. 

 


   

