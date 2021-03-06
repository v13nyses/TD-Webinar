//
// event.js
//
// This file is used on the event pages to control transitions between event
// states (from lobby to live, etc), syncing the video for pseudo-live streaming,
// and switching slides in a presentation.
//

// PresentationController listens for events from the video player, and switches slides.
// {{{
PresentationController = function(player, updateEngagement) {
  // queuePoints contains the slide timing and ids (used for ajax loading of slides)
  this.queuePoints = TDWebinar.settings.eventPage.queuePoints;
  this.engagementUpdateInterval = TDWebinar.settings.eventPage.engagementUpdateInterval;
  this.startTime = TDWebinar.settings.eventPage.startOffset;
  this.eventId = TDWebinar.settings.eventPage.id;
  this.lastEngagementUpdate = 0;
  this.currentQueuePoint = 0;
  //this.debug = true;
  this.debug = false;

  if(typeof(updateEngagement) == "undefined" || !updateEngagement) {
    this.trackEngagement = false;
  } else {
    this.trackEngagement = true;
  }

  this.initPlayer(player);
}

o = PresentationController.prototype;

o.initPlayer = function(player) {
  this.player = player;
  this.attachPlayerEvents();

  if(this.queuePoints.length > 1) {
    this.preloadSlide(1);
  }

  if(this.trackEngagement) {
    this.updateEngagement(this.startTime)
  }
}

o.attachPlayerEvents = function() {
  if(this.debug) {
    console.log('attaching events', this.player);
  }

  var self = this;
  // the onTime event is called every ~10ms
  this.player.onTime(function(event) {
    self.onTime(event);
  });
}

o.onTime = function(event) {
  this.loadSlide(event);

  if(this.trackEngagement) {
    var engagementUpdateDiff = event.position - this.lastEngagementUpdate;
    if(engagementUpdateDiff > this.engagementUpdateInterval) {
      this.lastEngagementUpdate = event.position;
      this.updateEngagement(event.position);
    }
  }
}

o.updateEngagement = function(duration) {
  var durationInt = Math.round(duration);
  engagementUrl = "/event/" + this.eventId + "/engagement/" + this.startTime + "/" + durationInt;
  $.ajax({
    url: engagementUrl,
    dataType: 'json',
    success: function(data) {
      // do nothing
    }
  });
}

o.attachPollEvents = function() {
  $(".poll form").submit(function() {
    var form = this;
    // submit the data with ajax
    $.ajax({
      url: $(form).attr("action"),
      dataType: 'json',
      data: $(form).serialize(),
      type: 'post',
      success: function(data) {
      }
    });
    $(form).html("Thank you for your input.");

    $(".poll form input").attr("disabled", "disabled");

    return false;
  });
}

o.slideUrl = function(queuePoint) {
  if(queuePoint == undefined) {
    queuePoint = this.currentQueuePoint;
  }
  var slideId = this.queuePoints[queuePoint].slideId;
  var url = TDWebinar.settings.eventPage.slideUrl + slideId + "/";
  return url;
}

o.loadSlide = function(event) {
  var queuePoint = this.queuePoints[this.currentQueuePoint];
  var lastQueuePoint = this.currentQueuePoint;
  var self = this;

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
    $(TDWebinar.settings.eventPage.slideshowContainer).load(this.slideUrl(), function() {
      self.attachPollEvents();
    });
    this.preloadSlide(nextQueuePoint);
  }
}

o.preloadSlide = function(queuePointNum) {
  if(queuePointNum < this.queuePoints.length) {
    $(TDWebinar.settings.eventPage.slideshowPreloadContainer).load(this.slideUrl(queuePointNum));
  }
}
// }}}

function f() {
  alert("aoeu");
  $(TDWebinar.settings.eventPage.engagementContainer).load(
    TDWebinar.settings.eventPage.engagementUrl() + "10/");
}

// EventController loads new event states and animates the transitions. It also sets
// up a PresentationController when necessary to control the slides.
// {{{
EventController = function() {
  this.presentationController = null;
  // call the onChangeState callback to setup variables
  this.onChangeState();
  this.setupStateTransitions();
  this.attachQuestionEvents();
}

o = EventController.prototype;

o.onChangeState = function() {
  this.tabController = TDWebinar.tabController;

  this.presentation = $(TDWebinar.settings.eventPage.presentationContainer);
  this.presentationWrapper = $(TDWebinar.settings.eventPage.presentationWrapper);

  this.state = TDWebinar.settings.eventPage.state;
  this.slideAnimationDuration = TDWebinar.settings.eventPage.slideAnimationDuration;
  this.presentationUrl = TDWebinar.settings.eventPage.presentationUrl;
  this.startOffset = TDWebinar.settings.eventPage.startOffset;

  if(this.state == 'live') {
    this.tabController.selectTab('.infotab.presenter-info');
    this.recordEngagement();
  } else {
    this.tabController.selectTab('.infotab.webinar-info');
  }
}

o.recordEngagement = function() {
  setInterval("f()", 10000);
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
    var randomNum = Math.round(Math.random() * 99999);
    var url = self.presentationUrl + '/' + randomNum;
    self.presentationWrapper
      .load(url, function(data) {
        self.onChangeState();
        self.attachQuestionEvents();
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
  this.startOffset = TDWebinar.settings.eventPage.startOffset;
  this.player = player;
  this.coverPlayer(false);
  if(this.state == 'live') {
    if(this.startOffset < this.player.getDuration() && this.startOffset > 0) {
      this.player.seek(this.startOffset);
    }
    this.startPresentation(true);
    this.coverPlayer(true);
    this.player.play();
  } else if(this.state == 'archive') {
    this.startPresentation();
  } else if(this.state == 'lobby') {
    this.coverPlayer(true);
    this.player.play();
  }
}

o.attachQuestionEvents = function() {
  // show a thank you message when the question form is submitted
  $("#questionform").submit(function() {
    // submit the data with ajax
    $.ajax({
      url: $("#questionform").attr("action"),
      dataType: 'json',
      data: $("#questionform").serialize(),
      type: 'post',
      success: function(data) {
      }
    });

    $("#questionform label").fadeOut(500, function() {
      var oldHtml = $("#questionform label").html();
      $("#questionform label")
        .html("Thank you for submitting your question")
        .fadeIn(500, function() {
          setTimeout(function() {
            $("#questionform label").fadeOut(500, function() {
              $("#questionform label").html(oldHtml).fadeIn();
              $("#questionform-right").fadeIn();
            });
          }, 2000);
        });
    });
    $("#questionform-right").fadeOut(500, function() {
      $("#questionform-right #question").val('');
    });

    return false;
  });
}

o.startPresentation = function(trackEngagementRaw) {
  var trackEngagement = typeof(trackEngagementRaw) != 'undefined' && trackEngagementRaw == true;
  if(!this.presentationController) {
    this.presentationController = new PresentationController(this.player, trackEngagement);
  } else {
    this.presentationController.trackEngagement = trackEngagement;
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

function clickListener() {
  // do nothing
}

// }}}

// TabController
// {{{
TabController = function(tabContainer, tabDefaultState, tabHoverState) {
  this.tabDefaultState = tabDefaultState;
  this.tabHoverState = tabHoverState;
  this.tabs = $(tabContainer).find("div");
  this.tabContainer = $(tabContainer);

  this.initPositions();
  this.attachEvents();
}

o = TabController.prototype;

o.attachEvents = function() {
  var self = this;
  this.tabs.hoverIntent(function() {
    self.onMouseOverTab(this);
  }, function() {
    self.onMouseOutTab(this);
  });

  this.tabs.click(function() {
    self.onTabClick(this);
  });
}

o.initPositions = function() {
  // set the positions when created, since IE won't use the initial css values
  this.tabs.each(function() {
    if(!$(this).hasClass('active')) {
      $(this)[0].style.backgroundPosition = '110px top';
    } else {
      $(this)[0].style.backgroundPosition = '50px top';
    }
  });
}

o.onMouseOverTab = function(tab) {
  if(!$(tab).hasClass("selected")) {
    $(tab).animate(this.tabHoverState);
  }
}

o.onMouseOutTab = function(tab) {
  if(!$(tab).hasClass("selected")) {
    $(tab).animate(this.tabDefaultState);
  }
}

o.onTabClick = function(tab) {
  this.selectTab(tab);
}

o.selectTab = function(tab) {
  tab = $(tab);
  if(!tab.hasClass("selected")) {
    // hide the content from other tabs
    var oldContainer = $('#' + this.tabContainer.find("div.selected").attr('rel'));
    var newContainer = $('#' + tab.attr('rel'));
    oldContainer.fadeOut(200, function() {
      newContainer.fadeIn(200);
    });


    this.tabContainer.find("div.selected")
      .animate(this.tabDefaultState)
      .removeClass("selected").removeClass("active");

    tab.addClass("selected").addClass("active").animate(this.tabHoverState);
  }
}
// }}}

$(document).ready(function() {
  TDWebinar.tabController = new TabController(TDWebinar.settings.eventPage.tabContainer,
                                              TDWebinar.settings.eventPage.tabDefaultState,
                                              TDWebinar.settings.eventPage.tabHoverState);
  // setup the event controller
  TDWebinar.eventController = new EventController();

  // add the fancybox popup for bios on the presenters tab
  $("#presenters a, #recommend-link").fancybox({width: 600, autoDimensions: false, scrolling: 'no'});

  // ajaxify the recommend form
  $("#recommend_form").submit(function() {
    $.ajax({
      url: $("#recommend_form").attr("action"),
      dataType: 'json',
      data: $("#recommend_form").serialize(),
      type: 'post',
      success: function(data) {
        // do nothing
      }
    });
    $.fancybox.close();

    return false;
  });
});
