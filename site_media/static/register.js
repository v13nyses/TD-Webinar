$(document).ready(function() {
  $("#register_event_form .register_for_event").click(function() {  
    var form = $("#register_event_form");
    $("#register_event_form input[name=email]").val($("#request.session.login_email"));
    $("#register_event_form input[name=event]").val($("#request.session.event_id"));
    form.submit();
  });
});
