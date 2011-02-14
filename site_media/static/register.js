$(document).ready(function() {
  $("#register_form .register_link").click(function() {
    var form = $("#register_form");
    $("#register_form input[name=register]").val("true");
    form.submit();
  });
});
