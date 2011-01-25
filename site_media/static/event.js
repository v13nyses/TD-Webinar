// called when the video player starts playing. Set up slide syncing
function playerReady(obj) {
  var queuePoints, queuePoint;
  var player = jwplayer(document.getElementById(obj.id));

  // load our queue points as JSON
  $.getJSON(TDWebinar.event.queuePointUrl, function(data) {
    queuePoints = data;
    queuePoint = queuePoints.pop();
  });

  // setup the onTime event for the player
  player.onTime(function(event) {
    if(typeof queuePoint != "undefined") {
      var slideUrl;
      while(event.position > queuePoint.timeOffset || queuePoint.timeOffset == 0) {
        // uncomment to debug
        //console.log("switching slide to: " + queuePoint.slideId);
        slideUrl = TDWebinar.event.slideUrl + queuePoint.slideId + "/";
        queuePoint = queuePoints.pop();
      }
      // put this outside the while, so we don't flash slides that don't need to be shown
      $(TDWebinar.settings.slideshowContainer).load(slideUrl);
    }
  });

  // check the current event state
  if(TDWebinar.event.state == 'live') {
    player.seek(TDWebinar.event.startOffset).play();
  } else {
    $("#presentation-cover").hide();
  }
}

$(document).ready(function() {
  // information and presenter tabs
  $("#information-tabs div")
    .hoverIntent(
      function() {
        if(!$(this).hasClass('selected')) {
          $(this).animate({
            'background-position': '50px top'
          }).addClass("active");
        }
      }, function() {
        if(!$(this).hasClass('selected')) {
          $(this).animate({
            'background-position': '110px top'
          }).removeClass("active");
        }
      })
    .click(function() {
      if(!$(this).hasClass("selected")) {
        // hide the content from other tabs
        var oldContainer = $("#information-tabs div.selected").attr('rel');
        $('#' + oldContainer).hide();

        $("#information-tabs div.selected")
          .removeClass("selected").removeClass("active")
          .animate({
            'background-position': '110px top'
          });

        $(this).addClass("selected").addClass("active");
        $('#' + $(this).attr('rel')).show();
      }
    });

  // add the fancybox popup for bios on the presenters tab
  $("#presenters a").fancybox();

  // show a thank you message when the question form is submitted
  $("#questionform").submit(function() {
    $("#questionform label").html("Thank you for submitting your question.");
    $("#questionform-right").hide();
    return false;
  });
});
