var dashboard = TDWebinar.settings.dashboard;

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
    console.log('changed');
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
  this.player.load(this.getUrl());
}

o.getUrl = function() {
  return dashboard.videoPlayerBaseUrl + this.video_id.val() + '/'
                                      + this.player_id.val() + '/';
}

$(document).ready(function() {
  $(dashboard.dateFields).datepicker({dateFormat: 'yy-mm-dd'});
  $(dashboard.videoWidget).each(function() {
    videoWidgets = new VideoWidget(this);
  });
  $(dashboard.previewStateLinks).find("a").click(function() {
    var url = $(this).attr('href').substring(1);
    $(dashboard.previewIframe).attr('src', url);
  });
});
