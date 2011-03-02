$(document).ready(function() {
  $("#presenters a").fancybox({width: 600, autoDimensions: false, scrolling: 'no'});
  $("#register_form .register_link").click(function() {
    var form = $("#register_form");
    $("#register_form input[name=register]").val("true");
    form.submit();
  });
});
