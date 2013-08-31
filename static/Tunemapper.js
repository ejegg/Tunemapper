function Tunemapper(lastFmUrl, positions) {
	this.positions = positions;
	this.lastFmUrl = lastFmUrl;
	this.map;
	this.player;
	this.infoWindow;
	
	var that = this; 
	
	this.initialize = function() {
	  google.maps.visualRefresh = true;
	  var mapOptions = {
	    mapTypeId: google.maps.MapTypeId.ROADMAP
	  };
	  that.map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
	  that.infoWindow = new google.maps.InfoWindow();
	  google.maps.event.addListener(that.map, 'click', function() { that.infoWindow.close() });

	  that.player = document.createElement('audio');
	  that.player.autoplay = true;
	  that.player.controls = true;

	  var pop = document.createElement('div');
	  pop.class = "pop";
	  pop.innerHTML = "<b>Trips</b>";
	  pop.style.backgroundColor = 'white';
	  pop.style.padding = '1px 6px';
	  pop.style.margin = '5px';
	  pop.style.fontFamily = 'Roboto, Arial, sans-serif';
	  pop.style.fontSize = '14px';
	  pop.style.cursor = 'pointer';
	  pop.style.border = 'solid grey 1px';
	  google.maps.event.addDomListener(pop, 'click', function() {
	    $("#picker").dialog({modal:true});
	  });
	  
	  that.map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(pop);
	  makeMarkers();
	  addTracks();
	  
	  $("#picker select").change(function() { 
	    $("#loading").show();
	    $.getJSON("/trips/" + $("#picker select option:selected").val(), function(data) {
	      $("#loading").hide();
	      $("#picker").dialog('close');
	      that.speedPath.setMap(null);
	      clearTrip();
	      that.positions = data; 
	      makeMarkers();
	      addTracks();
	    }); 
	  });
	}

	function clearTrip() {
	  that.map.controls[google.maps.ControlPosition.TOP_CENTER].clear();
	  var positions = that.positions;
	  var i = 0;
	  var pts = positions.length;
	  for(; i < pts; i++) {
	    var marker = positions[i].marker;
	    if (marker) {
	      marker.unbindAll();
	      marker.setMap(null);
	    }
	  }
	}

	function makeMarkers() {
	  var positions = that.positions;
	  var j = 0;
	  var pts = positions.length;
	  var bounds = new google.maps.LatLngBounds();
	  for (;j<pts;j++) {
	    var currentPos = positions[j];
	    currentPos.latLong = new google.maps.LatLng(currentPos.lat, currentPos.long);
	    bounds.extend(currentPos.latLong);
	  }
	  that.map.fitBounds(bounds);
	  that.speedPath = new SpeedPathOverlay(that.map, positions, bounds);
	}

	function addTracks() {
	  var tracks;
	  var fromTo = 'from=' + positions[0].time + '&to=' + positions[positions.length - 1].time;
	  if (supports_html5_storage()) {
	    tracks = localStorage.getItem(fromTo);
	    if (tracks) {
	      addTrackData(JSON.parse(tracks));
	      return;
	    }
	  }
	  var lfmUrl = that.lastFmUrl + '&' + fromTo + '&format=json';
	  $.getJSON(lfmUrl, null, function(data) {
	    tracks = data.recenttracks.track || [];
	    if (supports_html5_storage()) {
	      localStorage.setItem(fromTo, JSON.stringify(tracks));
	    }
	    addTrackData(tracks);
	    that.speedPath.draw(); //redraw since we'll have nice colors on it now
	  });
	}

	function addTrackData(tracks) {
	  var positions = that.positions;
	  var map = that.map;
	  var i = 0;
	  var pts = positions.length;
	  var lastTrack;
	  var cols = [ [25,0,0], [25, 25, 0], [0,25,0], [5,5,25] ];
	  var colIndex = 0;
	  var currentColor = cols[0];
	  var lastChangeIndex = 0;
	  var iconSize = new google.maps.Size(34, 34);
	  
	  for (;i<pts;i++) {
	    var currentPos = positions[i];
	    var listenTime = currentPos.time;
	    var currentTrack = getCurrentTrack(tracks, listenTime);
	    currentPos.color = [50 + currentColor[0] * currentPos.spd, 50 + currentColor[1] * currentPos.spd, 50 + currentColor[2] * currentPos.spd];

	    if (currentTrack) {
	      if (i == pts -1 || !lastTrack || lastTrack.artist != currentTrack.artist || lastTrack.name != currentTrack.name) {
	        colIndex = (colIndex + 1) % (cols.length);
	        currentColor = cols[colIndex];

	        var midpoint = positions[Math.round((i + lastChangeIndex) / 2)];

	        var markerOpts = {
	            position: midpoint.latLong,
	            map: that.map,
	            title: lastTrack ? "Listening to " + lastTrack.name + " by " + lastTrack.artist : "Nothing scrobbled"
	        }
	        midpoint.marker = new google.maps.Marker(markerOpts);
	        if (lastTrack && lastTrack.smallPic != "") {
	            midpoint.marker.setIcon({ url: lastTrack.smallPic, size: iconSize });
	        }
	        makeInfoWindow(midpoint, lastTrack);

	        lastChangeIndex = i;
	        lastTrack = currentTrack;
	      }
	    } else {
	      var c = 25 * currentPos.spd;
	      currentPos.color = [c,c,c];
	    }

	  }
	}

	function getCurrentTrack(tracks, listenTime) {
	  var numTracks = tracks.length;
	  var i = 0;
	  for (;i < numTracks; i++) {
	    var track = tracks[i];
	    if (track.date && listenTime > parseInt(track.date.uts)) {
	      return {
	        name: track.name,
	        artist: track.artist['#text'],
	        smallPic: track.image[0]['#text'],
	        largePic: track.image[2]['#text']
	      };
	    }
	  }
	  return null;
	}

	function makeInfoWindow(position, track) {
	    var marker = position.marker;
	    var txt = "<table><tr><td><ul><li>Time: " + new Date(position.time * 1000) + "</li>" + 
	             "<li>Speed: " + (position.spd * 2.237) + " mph</li>";
	    if (track) {
	        txt += "<li>Track: " + track.name + "</li>" + 
	               "<li>Artist: " + track.artist + "</li>";
	    }

	    txt += "</ul></td>";

	    if (track && track.largePic != "") {
	        txt += "<td><div class='analbumcover'><img src='" + track.largePic + "'></div></td>";
	    }

	    txt += "</tr></table>";

	    google.maps.event.addListener(marker, 'click', function() {
	        that.infoWindow.setContent(txt);
	        that.infoWindow.open(that.map, marker);
	        if (track) {
	            $.getJSON('/tracks/' + track.artist + '/' + track.name, function(data) {
	                if (data && data != "-1") {
	                	that.map.controls[google.maps.ControlPosition.TOP_CENTER].clear();
	                	that.player.src ='/tracks/' + data
	                	that.map.controls[google.maps.ControlPosition.TOP_CENTER].push(that.player);
	                }
	            });
	        }
	    });
	}

	function supports_html5_storage() {
	  try {
	    return 'localStorage' in window && window['localStorage'] !== null;
	  } catch (e) {
	    return false;
	  }
	}
	
	return {
		initialize: this.initialize
	}
}