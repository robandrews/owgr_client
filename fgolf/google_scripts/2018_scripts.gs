// FINAL
function checkTrades(){
  const LEAGUE_EMAILS = ["Rob Andrews <robert.alan.andrews@gmail.com>", 
                         "Greg Sund <gmsund@gmail.com>", 
                         "Kamal Yechoor <kamal.yechoor@gmail.com>",
                         "Eric Porter <ecporter04@gmail.com>",
                         "Patrick Kochyan <patrick.kochyan@gmail.com>",
                         "Tom Klun <thomas.a.klun@gmail.com>"
                        ];
  const LEAGUE_TRADE_COLORS = ["#FFFFFF", "#3D79D2", "#D2A927", "#C50400", "#69A751", "#674EA9", "#468190"];
  const HASH_PROP_KEY = "FG_2018_TRADES";
  var scriptProperties = PropertiesService.getScriptProperties();
  var sheet = SpreadsheetApp.openByUrl("https://docs.google.com/spreadsheets/d/1RkD-QQJu4WRzoZGyvhH3_BwvgT4a-jWjfUwe1QviP7A/edit#gid=2008094694").getSheetByName("Trades");
  var range = sheet.getRange("B2:H53");
  
  var hashValue = hash(range.getDisplayValues());
  var prop = scriptProperties.getProperty(HASH_PROP_KEY);
  if(hashValue == prop) return;
  scriptProperties.setProperty(HASH_PROP_KEY, hashValue);
  GmailApp.sendEmail(LEAGUE_EMAILS.join(', '), "Trades Table Updated", "Enable HTML in your email client to view this message", {htmlBody: createTradeHtmlTable(range, LEAGUE_TRADE_COLORS)});
}

// Review, 6/31
function checkAddDrop(){
  const LEAGUE_EMAILS = ["Rob Andrews <robert.alan.andrews@gmail.com>", 
                       "Greg Sund <gmsund@gmail.com>", 
                       "Kamal Yechoor <kamal.yechoor@gmail.com>",
                       "Eric Porter <ecporter04@gmail.com>",
                       "Patrick Kochyan <patrick.kochyan@gmail.com>",
                       "Tom Klun <thomas.a.klun@gmail.com>"
                        ];
  const LEAGUE_TRADE_COLORS = ["#3D79D2", "#D2A927", "#C50400", "#69A751", "#674EA9", "#468190"];
  const HASH_PROP_KEY = "FG_2018_ADD_DROP";
  var scriptProperties = PropertiesService.getScriptProperties();
  var sheet = SpreadsheetApp.openByUrl("https://docs.google.com/spreadsheets/d/1RkD-QQJu4WRzoZGyvhH3_BwvgT4a-jWjfUwe1QviP7A/edit#gid=1310768896").getSheetByName("A/Ds and Rentals");
  var range = sheet.getRange("A2:R18");
  
  var hashValue = hash(range.getDisplayValues());
  var prop = scriptProperties.getProperty(HASH_PROP_KEY);
  if(hashValue == prop) return;
  scriptProperties.setProperty(HASH_PROP_KEY, hashValue);
  GmailApp.sendEmail(LEAGUE_EMAILS.join(', '), "Add/Drop Table Updated", "Enable HTML in your email client to view this message", {htmlBody: createAddDropHtmlTable(range, LEAGUE_TRADE_COLORS)});
}

// Reviewed 6/31
function checkRentals(){
  const LEAGUE_EMAILS = ["Rob Andrews <robert.alan.andrews@gmail.com>", 
                         "Greg Sund <gmsund@gmail.com>", 
                         "Kamal Yechoor <kamal.yechoor@gmail.com>",
                         "Eric Porter <ecporter04@gmail.com>",
                         "Patrick Kochyan <patrick.kochyan@gmail.com>",
                         "Tom Klun <thomas.a.klun@gmail.com>"
                        ];
  const LEAGUE_TRADE_COLORS = ["#3D79D2", "#D2A927", "#C50400", "#69A751", "#674EA9", "#468190"];
  const HASH_PROP_KEY = "FG_2018_RENTALS";
  var scriptProperties = PropertiesService.getScriptProperties();
  var sheet = SpreadsheetApp.openByUrl("https://docs.google.com/spreadsheets/d/1RkD-QQJu4WRzoZGyvhH3_BwvgT4a-jWjfUwe1QviP7A/edit#gid=1310768896").getSheetByName("A/Ds and Rentals");
  var range = sheet.getRange("A21:R36");
  
  var hashValue = hash(range.getDisplayValues());
  var prop = scriptProperties.getProperty(HASH_PROP_KEY);
  if(hashValue == prop) return;
  scriptProperties.setProperty(HASH_PROP_KEY, hashValue);
  GmailApp.sendEmail(LEAGUE_EMAILS.join(', '), "Rentals Table Updated", "Enable HTML in your email client to view this message", {htmlBody: createRentalsHtmlTable(range, LEAGUE_TRADE_COLORS)});
}

// Buffer
// to
// add
// lines
// to
// see 
// if
// line number changes
function hash(input){
  return Utilities.computeDigest(Utilities.DigestAlgorithm.MD5, input.toString()).toString();
}

function rowIsEmpty(range, rowInt){
  for(var z = 1; z <= range.getWidth(); z++){
    var val = range.getCell(rowInt, z).getValue();
    if(val != '') return false;
  }
  return true;
}


function createTradeHtmlTable(range, colors){
  var htmlStr = "<p style='font-size:1.1em'>The <a href='https://docs.google.com/spreadsheets/d/1RkD-QQJu4WRzoZGyvhH3_BwvgT4a-jWjfUwe1QviP7A/edit#gid=2008094694'>trades table</a> has changed:</p><br /><table style='border: 1px solid black; border-collapse:collapse;'><tr>";
  for(var j = 0; j < range.getWidth(); j++){
    htmlStr += "<th bgcolor='" + colors[j] + "' style='border: 1px solid black; padding:4px;'>" + range.getCell(1,j+1).getValue() + "</th>";
  }
  htmlStr += "</tr>";
  
  for (var i = 2; i <= range.getHeight(); i++){
    if (rowIsEmpty(range, i)) continue;
    htmlStr += "<tr>";
    for (var j = 1; j <= range.getWidth(); j++){
      if(j == 1){
        htmlStr += "<td style='border: 1px solid black; padding:4px;'>" + Utilities.formatDate(new Date(range.getCell(i,j).getValue()), "PST", "EEE, MMM dd") + "</td>";
      }else{
        htmlStr += "<td style='border: 1px solid black; padding:4px;'>" + range.getCell(i,j).getValue() + "</td>";
      }
    }
    htmlStr += "</tr>";
  }
  htmlStr += "</table><br />"
  return htmlStr;
}


function createAddDropHtmlTable(range, colors){
  var htmlStr = "<p style='font-size:1.1em'>The <a href='https://docs.google.com/spreadsheets/d/1RkD-QQJu4WRzoZGyvhH3_BwvgT4a-jWjfUwe1QviP7A/edit#gid=1310768896'>add drop board</a> has changed:</p><br /><table style='border: 1px solid black; border-collapse:collapse;'><tr>";
  for(var j = 0; j < range.getWidth()/3; j++){
    htmlStr += "<th colspan='3' bgcolor='" + colors[j] + "' style='border: 1px solid black; padding:4px;'>" + range.getCell(1,3*j+1).getValue() + "</th>";
  }
  htmlStr += "</tr>";
  
  for (var i = 2; i <= range.getHeight(); i++){
    if (rowIsEmpty(range, i)) continue;
    htmlStr += "<tr>";
    for (var j = 1; j <= range.getWidth(); j++){
      htmlStr += "<td style='border: 1px solid black; padding:4px;'>" + range.getCell(i,j).getValue() + "</td>";
    }
    htmlStr += "</tr>";
  }
  htmlStr += "</table><br />"
  return htmlStr;
}


function createRentalsHtmlTable(range, colors){
  var htmlStr = "<p style='font-size:1.1em'>The <a href='https://docs.google.com/spreadsheets/d/1RkD-QQJu4WRzoZGyvhH3_BwvgT4a-jWjfUwe1QviP7A/edit#gid=1310768896'>rentals board</a> has changed:</p><br /><table style='border: 1px solid black; border-collapse:collapse;'><tr>";
  for(var z = 0; z < 2; z++){
    // Headers
    for(var j = 0; j < range.getWidth()/6; j++){
      htmlStr += "<th colspan='6' bgcolor='" + colors[j+(3*z)] + "' style='border: 1px solid black; padding:4px;'>" + range.getCell(1 + (z*8), 6*j+1).getValue() + "</th>";
    }
    htmlStr += "</tr>";
    
    // Data rows
    for (var i = 2 + (z*8); i <= 8 * (z+1); i++){
      if (rowIsEmpty(range, i)) continue;
      htmlStr += "<tr>";
      for (var j = 1; j <= range.getWidth(); j++){
        htmlStr += "<td style='border: 1px solid black; padding:4px;'>" + range.getCell(i,j).getValue() + "</td>";
      }
      htmlStr += "</tr>";
    }
    
  }
  htmlStr += "</table><br />"
  return htmlStr;
}
