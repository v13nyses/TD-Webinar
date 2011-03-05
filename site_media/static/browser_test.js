// Find out what cookies are supported. Returns:
// null - no cookies
// false - only session cookies are allowed
// true - session cookies and persistent cookies are allowed
// (though the persistent cookies might not actually be persistent, if the user has set
// them to expire on browser exit)
//
function getCookieSupport() {
    var persist= true;
    do {
        var c= 'gCStest='+Math.floor(Math.random()*100000000);
        document.cookie= persist? c+';expires=Tue, 01-Jan-2030 00:00:00 GMT' : c;
        if (document.cookie.indexOf(c)!==-1) {
            document.cookie= c+';expires=Sat, 01-Jan-2000 00:00:00 GMT';
            return persist;
        }
    } while (!(persist= !persist));
    return null;
}

var pass = function(container) {
  setTimeout(function() {
    $(".browser-tests").find(container)
      .addClass("passed")
      .find("span")
        .html("passed")
  }, 1000);
}

var fail = function(container, message) {
  setTimeout(function() {
    $(".browser-tests").find(container)
      .addClass("failed")
      .find("span")
        .html(message);
  }, 1000);
}

$(document).ready(function() {
  var flashVersion = swfobject.getFlashPlayerVersion();
  var browser = $.browser;

  if(typeof(browser.msie) == 'undefined' || parseInt(browser.version) >= 6) {
    pass(".browser");
  } else {
    fail(".browser", "FAILED: Internet Explorer 7 or greater required.");
  }

  if(flashVersion.major >= 9) {
    pass(".flash");
  } else {
    fail(".flash", "FAILED: Flash 9 or greater required");
  }

  if(getCookieSupport() !== null) {
    pass(".cookies");
  } else {
    fail(".cookies", "FAILED: Cookies must be enabled.");
  }

  pass(".javascript");
}); 
