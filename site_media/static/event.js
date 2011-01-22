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
        console.log("switching slide to: " + queuePoint.slideId);
        var slideUrl = TDWebinar.event.slideUrl + queuePoint.slideId;
        $(TDWebinar.settings.slideshowContainer).load(slideUrl);
        queuePoint = queuePoints.pop();
      }
    }
  });
}
