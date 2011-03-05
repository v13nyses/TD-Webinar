TDWebinar = {
  settings: {
    dashboard: {
      dateFields: "#id_lobby_start_date_0, #id_live_start_date_0, #id_live_stop_date_0, #id_archive_start_date_0",
      videoWidget: ".video-widget-container",
      bitsOnTheRunBaseUrl: "http://content.bitsontherun.com/players/",
      videoPlayerBaseUrl: "/presentation/video-player/",
      playerUpdateInterval: 2000,
      previewStateLinks: ".preview-fieldset ul.preview-states",
      previewIframe: ".preview-fieldset iframe"
    },
    eventPage: { 
      slideshowContainer: "#slideshow",
      slideshowPreloadContainer: "#slideshow-preload",
      presentationWrapper: "#presentation-wrapper",
      presentationContainer: "#presentation",
      playerCover: "#presentation-cover",
      eventStates: ["pre", "lobby", "live", "post", "archive"],
      slideAnimationDuration: 800,
      tabContainer: "#information-tabs",
      tabDefaultState: {backgroundPosition: '110px top'},
      tabHoverState: {backgroundPosition: '50px top'},
      engagementUpdateInterval: 60,
    }
  }
}
