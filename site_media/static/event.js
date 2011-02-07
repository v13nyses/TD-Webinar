// called when the video player starts playing. Set up slide syncing
function playerReady(obj) {
  var queuePoints, queuePoint;
  var player = jwplayer(document.getElementById(obj.id));

  // load our queue points as JSON
  $.getJSON(TDWebinar.settings.eventPage.queuePointUrl, function(data) {
    queuePoints = data;
    queuePoint = queuePoints.pop();
  });

  // setup the onTime event for the player
  player.onTime(function(event) {
    if(typeof queuePoint !== "undefined") {
      var slideUrl;
      while(event.position > queuePoint.timeOffset || queuePoint.timeOffset == 0) {
        slideUrl = TDWebinar.settings.eventPage.slideUrl + queuePoint.slideId + "/";
        queuePoint = queuePoints.pop();
      }
      // put this outside the while, so we don't flash slides that don't need to be shown
      $(TDWebinar.settings.slideshowContainer).load(slideUrl);
    }
  });

  // check the current event state
  if(TDWebinar.settings.eventPage.state == 'live') {
    player.seek(TDWebinar.settings.eventPage.startOffset).play();
  } else {
    $("#presentation-cover").hide();
  }
}

EventController = function() {
  this.reloadElements();
  this.setupStateTransitions();
}

o = EventController.prototype;

o.reloadElements = function() {
  this.presentation = $(TDWebinar.settings.eventPage.presentationContainer);
  this.presentationWrapper = $(TDWebinar.settings.eventPage.presentationWrapper);
  this.state = TDWebinar.settings.eventPage.state;
  this.slideAnimationDuration = TDWebinar.settings.eventPage.slideAnimationDuration;
  this.presentationUrl = TDWebinar.settings.eventPage.presentationUrl;
}

o.stateNum = function() {
  var states = TDWebinar.settings.eventPage.eventStates;
  var currentState = TDWebinar.settings.eventPage.state;
  for(var i = 0; i < states.length; i++) {
    if(states[i] == currentState) {
      return i;
    }
  }
  return -1;
}

o.setupStateTransitions = function() {
  var states = TDWebinar.settings.eventPage.eventStates;
  var stateOffsets = TDWebinar.settings.eventPage.stateTransitionOffsets;
  var self = this, offset;
  for(var i = 0; i < states.length; i++) {
    offset = stateOffsets[states[i]];
    if(offset > -1) {
      (function() {
        var state = states[i];
        console.log(state);
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
        self.reloadElements();
        self.presentation.hide().slideDown(self.slideAnimationDuration);
      });
  }
  if(this.presentation.length == 0) {
    loadNewState();
  } else {
    this.presentation.slideUp(this.slideAnimationDuration, loadNewState);
  }
}

$(document).ready(function() {
  // setup the event controller
  eventController = new EventController();
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
