$(document).ready(function() {
  $("#logout_form .logout_link").click(function() {  
    var form = $("#logout_form");
    $("#logout_form input[name=logout]").val("true");
    form.submit();
  });
});
