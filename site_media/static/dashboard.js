dashboard = {
  dateFields: "#id_lobby_start_date_0, #id_live_start_date_0, #id_live_stop_date_0, #id_archive_start_date_0"
}

$(document).ready(function() {
  $(dashboard.dateFields).datepicker();
});
