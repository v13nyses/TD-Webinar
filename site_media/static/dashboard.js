dashboard = {
  dateFields: "#id_lobby_start_date_0, #id_live_start_date_0, #id_live_stop_date_0, #id_archive_start_date_0",
  videoWidget: ".video-widget-container",
  bitsOnTheRunBaseUrl: "http://content.bitsontherun.com/players/",
  videoPlayerBaseUrl: "/presentation/video-player/",
  playerUpdateInterval: 2000
}

VideoWidget = function(container) {
  this.container = $(container);
  this.video_id = this.container.find("input#lobby_video_0");
  this.player_id = this.container.find("input#lobby_video_1");
  this.player = this.container.find(".video-container");

  this.addCallbacks();
  this.onChange();
}

var o = VideoWidget.prototype;
o.addCallbacks = function() {
  var self = this;
  var changed = false;
  var change = function() {
    changed = true; 
  }
  var timer = function() {
    if(changed) {
      self.onChange();
      changed = false;
    }
  }
  setInterval(timer, dashboard.playerUpdateInterval);
  this.video_id.keyup(change);
  this.player_id.keyup(change);
}

o.onChange = function() {
  console.log(this.getUrl());
  //this.player.load(this.getUrl());
}

o.getUrl = function() {
  return dashboard.videoPlayerBaseUrl + this.video_id.val() + '/'
                                      + this.player_id.val() + '/';
}

$(document).ready(function() {
  $(dashboard.dateFields).datepicker({dateFormat: 'yy-mm-dd'});
  /* Don't enable the video widget JS until we figure out a way to 
   * control the embedded BitsOnTheRun player.
  $(dashboard.videoWidget).each(function() {
    videoWidgets = new VideoWidget(this);
  });
  */
});
