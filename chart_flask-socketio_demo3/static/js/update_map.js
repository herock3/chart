var GMaps_styles = (function(global) {
  "use strict";

  var GMaps_styles = function(options) {
    if (!this) return new GMaps_styles(options);

    if( typeof(options) == 'undefined' ){options = [];}
    options.custom_styles = options.custom_styles || [];

    var self = this;

    // Define styles
    this.data = [];

    this.data["light-political"] = {
      mapName : "\u00c9l\u00e9ments g\u00e9ographiques att\u00e9nu\u00e9s et fronti\u00e8res politiques",
      mapId   : "light-political",
      styles : [{
          featureType: "water",
          stylers: [{
              visibility: "on"
          }, {
              saturation: 2
          }, {
              hue: "#004cff"
          }, {
              lightness: 40
          }]
      }, {
          featureType: "administrative",
          elementType: "geometry",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "landscape",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 45
          }]
      }, {
          featureType: "transit",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "poi.government",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "poi",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "road",
          elementType: "labels",
          stylers: [{
              visibility: "off"
          }]
      }, {
          featureType: "road",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }, {
              saturation: -99
          }, {
              lightness: 60
          }]
      }, {
          featureType: "administrative.country",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 50
          }]
      }, {
          featureType: "administrative.province",
          elementType: "geometry",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 50
          }]
      }, {
          featureType: "administrative.country",
          elementType: "labels",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 50
          }]
      }, {
          featureType: "administrative.locality",
          elementType: "labels",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 60
          }]
      }, {
          featureType: "administrative.neighborhood",
          elementType: "labels",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 65
          }]
      }, {
          featureType: "administrative.province",
          elementType: "label",
          stylers: [{
              visibility: "on"
          }, {
              lightness: 55
          }]
      }]
    };

  };

  return GMaps_styles;
})(this);