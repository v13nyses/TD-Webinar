//
// event.js
//
// This file is used on the event pages to control transitions between event
// states (from lobby to live, etc), syncing the video for pseudo-live streaming,
// and switching slides in a presentation.
//

// PresentationController listens for events from the video player, and switches slides.
PresentationController = function(player) {
  // queuePoints contains the slide timing and ids (used for ajax loading of slides)
  this.queuePoints = TDWebinar.settings.eventPage.queuePoints;
  this.currentQueuePoint = 0;
  this.debug = true;

  this.initPlayer(player);
}

o = PresentationController.prototype;

o.initPlayer = function(player) {
  this.player = player;
  this.attachPlayerEvents();
}

o.attachPlayerEvents = function() {
  if(this.debug) {
    console.log('attaching events', this.player);
  }

  var self = this;
  // the onTime event is called every ~10ms
  this.player.onTime(function(event) {
    self.loadSlide(event);
  });
}

o.slideUrl = function() {
  var slideId = this.queuePoints[this.currentQueuePoint].slideId;
  return TDWebinar.settings.eventPage.slideUrl + slideId + "/";
}

o.loadSlide = function(event) {
  var queuePoint = this.queuePoints[this.currentQueuePoint];
  var lastQueuePoint = this.currentQueuePoint;

  var nextQueuePoint = this.currentQueuePoint + 1;
  if(queuePoint.timeOffset < event.position) {
    while(nextQueuePoint < this.queuePoints.length && 
          this.queuePoints[nextQueuePoint].timeOffset < event.position) {
      nextQueuePoint += 1;
      this.currentQueuePoint += 1;
    }
  } else if(queuePoint.timeOffset > event.position) {
    while(this.currentQueuePoint > 0 && 
          this.queuePoints[this.currentQueuePoint].timeOffset > event.position) {
      nextQueuePoint -= 1;
      this.currentQueuePoint -= 1;
    }
  }

  if(this.currentQueuePoint != lastQueuePoint) {
    $(TDWebinar.settings.eventPage.slideshowContainer).load(this.slideUrl());
  }
}

// EventController loads new event states and animates the transitions. It also sets
// up a PresentationController when necessary to control the slides.
EventController = function() {
  this.presentationController = null;
  // call the onChangeState callback to setup variables
  this.onChangeState();
  this.setupStateTransitions();
}

o = EventController.prototype;

o.onChangeState = function() {
  this.presentation = $(TDWebinar.settings.eventPage.presentationContainer);
  this.presentationWrapper = $(TDWebinar.settings.eventPage.presentationWrapper);

  this.state = TDWebinar.settings.eventPage.state;
  this.slideAnimationDuration = TDWebinar.settings.eventPage.slideAnimationDuration;
  this.presentationUrl = TDWebinar.settings.eventPage.presentationUrl;
  this.startOffset = TDWebinar.settings.eventPage.startOffset;
}

o.setupStateTransitions = function() {
  // grab a list of all possible states
  var states = TDWebinar.settings.eventPage.eventStates;
  // and an object containing the time (in seconds) to switch states
  var stateOffsets = TDWebinar.settings.eventPage.stateTransitionOffsets;
  var self = this;
  var offset;
  // loop through all the offsets, and 
  for(var i = 0; i < states.length; i++) {
    offset = stateOffsets[states[i]];
    if(offset > -1) {
      // use an anonymous function to create another scope for state, otherwise
      // it will get overwritten in the next loop iteration
      (function() {
        var state = states[i];
        // change the state in <offset> seconds
        setTimeout(function() {
          self.changeState(state);
        }, offset * 1000);
      })();
    }
  }
}

o.changeState = function(state) {
  // slide the presentation up, and hide the wrapper
  if(this.debug) {
    console.log("Changing states:", state);
  }
  var self = this;
  var loadNewState = function() {
    self.presentationWrapper
      .load(self.presentationUrl, function(data) {
        self.onChangeState();
        self.presentation.hide().slideDown(self.slideAnimationDuration);
      });
  }
  if(this.presentation.length == 0) {
    loadNewState();
  } else {
    this.presentation.slideUp(this.slideAnimationDuration, loadNewState);
  }
}

o.onPlayerReady = function(player) {
  this.player = player;
  console.log('onPlayerReady', player, this.state);
  if(this.state == 'live') {
    if(this.startOffset < this.player.getDuration() && this.startOffset > 0) {
      this.player.seek(this.startOffset);
    }
    this.startPresentation();
    this.coverPlayer(true);
    this.player.play();
  } else if(this.state == 'archive') {
    this.startPresentation();
    this.coverPlayer(false);
  } else {
    this.coverPlayer(false);
  }
}

o.startPresentation = function() {
  if(!this.presentationController) {
    this.presentationController = new PresentationController(this.player);
  } else {
    this.presentationController.initPlayer(this.player);
  }
}

o.coverPlayer = function(cover) {
  if(cover) {
    $(TDWebinar.settings.eventPage.playerCover).show();
  } else {
    $(TDWebinar.settings.eventPage.playerCover).hide();
  }
}

// called when the video player starts playing. Set up slide syncing
function playerReady(obj) {
  var player = jwplayer(document.getElementById(obj.id));
  TDWebinar.eventController.onPlayerReady(player);
}

$(document).ready(function() {
  // setup the event controller
  TDWebinar.eventController = new EventController();

  // information and presenter tabs
  $("#information-tabs div")
    .hoverIntent(
      function() { // mouse over
        if(!$(this).hasClass('selected')) {
          $(this).animate({
            'background-position': '50px top'
          }).addClass("active");
        }
      }, function() { // mouse out
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
