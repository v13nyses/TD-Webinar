// called when the video player starts playing. Set up slide syncing
function playerReady(obj) {
  var queuePoints, queuePoint;
  var player = document.getElementById(obj.id);

  // load our queue points as JSON
  $.getJSON(TDWebinar.event.queuePointUrl, function(data) {
    queuePoints = data;
    queuePoint = queuePoints.pop();
  });

  // setup the onTime event for the player
  jwplayer(player).onTime(function(event) {
    if(typeof queuePoint != "undefined") {
      if(event.position > queuePoint.timeOffset || queuePoint.timeOffset == 0) {
        // uncomment to debug
        //console.log("switching slide to: " + queuePoint.slideId);
        var slideUrl = TDWebinar.event.slideUrl + queuePoint.slideId + "/";
        $(TDWebinar.settings.slideshowContainer).load(slideUrl);
        queuePoint = queuePoints.pop();
      }
    }
  });
}

$(document).ready(function() {
  // information and presenter tabs
  $("#information-tabs div")
    .hoverIntent(
      function() {
        if(!$(this).hasClass('selected')) {
          $(this).animate({
            'background-position': '50px top'
          });
        }
      }, function() {
        if(!$(this).hasClass('selected')) {
          $(this).animate({
            'background-position': '110px top'
          });
        }
      })
    .click(function() {
      if(!$(this).hasClass("selected")) {
        // hide the content from other tabs
        var oldContainer = $("#information-tabs div.selected").attr('rel');
        $('#' + oldContainer).hide();

        $("#information-tabs div.selected")
          .removeClass("selected")
          .animate({
            'background-position': '110px top'
          });

        $(this).addClass("selected");
        $('#' + $(this).attr('rel')).show();
      }
    });

  // add the fancybox popup for bios on the presenters tab
  $("#presenters a").fancybox();
});
