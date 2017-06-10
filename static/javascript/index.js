  function myFunction() {
  	var optionsBox = document.getElementById('optionsBox');
  	var show = document.getElementById('optionsButton');
  	if (optionsBox.style.display !== 'block') {
  		optionsBox.style.display = 'block';
  		show.innerHTML = "hide options";
  	}
  	else {
  		optionsBox.style.display = 'none';
  		show.innerHTML = "show options";
  	}
  };


  var map;
  var markers = [];
  var polygon = null;

  function initMap() {
  	var styles = [
  	{
  		featureType: 'water',
  		stylers: [
  		{ color: '#19a0d8' }
  		]
  	},{
  		featureType: 'administrative',
  		elementType: 'labels.text.stroke',
  		stylers: [
  		{ color: '#ffffff' },
  		{ weight: 6 }
  		]
  	},{
  		featureType: 'administrative',
  		elementType: 'labels.text.fill',
  		stylers: [
  		{ color: '#e85113' }
  		]
  	},{
  		featureType: 'road.highway',
  		elementType: 'geometry.stroke',
  		stylers: [
  		{ color: '#efe9e4' },
  		{ lightness: -40 }
  		]
  	},{
  		featureType: 'transit.station',
  		stylers: [
  		{ weight: 9 },
  		{ hue: '#e85113' }
  		]
  	},{
  		featureType: 'road.highway',
  		elementType: 'labels.icon',
  		stylers: [
  		{ visibility: 'off' }
  		]
  	},{
  		featureType: 'water',
  		elementType: 'labels.text.stroke',
  		stylers: [
  		{ lightness: 100 }
  		]
  	},{
  		featureType: 'water',
  		elementType: 'labels.text.fill',
  		stylers: [
  		{ lightness: -100 }
  		]
  	},{
  		featureType: 'poi',
  		elementType: 'geometry',
  		stylers: [
  		{ visibility: 'on' },
  		{ color: '#f0e4d3' }
  		]
  	},{
  		featureType: 'road.highway',
  		elementType: 'geometry.fill',
  		stylers: [
  		{ color: '#efe9e4' },
  		{ lightness: -25 }
  		]
  	}
  	];

  	map = new google.maps.Map(document.getElementById('map'), {
  		center: {lat: 40.7413549, lng: -73.9980244},
  		zoom: 10,
  		styles: styles,
  		mapTypeControl: false
  	});
  	
  	var largeInfowindow = new google.maps.InfoWindow();
  	var drawingManager = new google.maps.drawing.DrawingManager({
  		drawingMode: google.maps.drawing.OverlayType.POLYGON,
  		drawingControl: true,
  		drawingControlOptions: {
  			position: google.maps.ControlPosition.TOP_LEFT,
  			drawingModes: [
  			google.maps.drawing.OverlayType.POLYGON
  			]
  		}
  	});

  	var defaultIcon = makeMarkerIcon('0091ff');
  	var highlightedIcon = makeMarkerIcon('FFFF24');
  	var episodeName = [];
  	var episodeDescription = [];
  	var timeTaken = [];
  	var coverPhoto = [];
  	var episodeIds = [];
  	markers = [];

          //get JSON object from the database
          $.getJSON('http://localhost:5000/episodes/JSON', function(data){
          	for (var i = 0; i < data.episodes.length;i++){
          		var position = new google.maps.LatLng(data.episodes[i].latitude, data.episodes[i].longitude);
          		episodeName.push(data.episodes[i].name);
          		episodeDescription.push(data.episodes[i].description);
          		timeTaken.push(data.episodes[i].timestamp);
          		episodeIds.push(data.episodes[i].id);
          		var title = data.episodes[i].name;
          		var filePath = "http://localhost:5000/photo/" + data.episodes[i].id + "/" + data.episodes[i].filename;
          		coverPhoto.push(filePath);


          		var marker = new google.maps.Marker({
          			position: position,
          			title: title,
          			animation: google.maps.Animation.DROP,
          			icon: defaultIcon,
          			id: i
          		});
          		markers.push(marker);              
          		marker.addListener('click', function() {
          			populateInfoWindow(this, largeInfowindow, episodeName, episodeDescription, timeTaken, coverPhoto, episodeIds);
          		});  
          		marker.addListener('mouseover', function() {
          			this.setIcon(highlightedIcon);
          		});
          		marker.addListener('mouseout', function() {
          			this.setIcon(defaultIcon);
          		}); 
          	}
          });
          document.getElementById('show-listings').addEventListener('click', showListings);
          document.getElementById('hide-listings').addEventListener('click', hideListings);
          document.getElementById('check-episodes').addEventListener('click', function() {
          	zoomToArea();
          });
          document.getElementById('check-by-name').addEventListener('click', function() {
          	zoomToEpisode();
          }); 
          
          drawingManager.addListener('overlaycomplete', function(event) {
          	if (polygon) {
          		polygon.setMap(null);
          		hideListings(markers);
          	}
          	drawingManager.setDrawingMode(null);
          	polygon = event.overlay;
          	polygon.setEditable(true);
          	searchWithinPolygon();
          	polygon.getPath().addListener('set_at', searchWithinPolygon);
          	polygon.getPath().addListener('insert_at', searchWithinPolygon);
          });
        }



        function populateInfoWindow(marker, infowindow,episodeName, episodeDescription, timeTaken, coverPhoto,episodeIds) {
        	var parentDiv = getParentDiv(episodeIds[marker.id], episodeName[marker.id], episodeDescription[marker.id], timeTaken[marker.id]);  
        	if (infowindow.marker != marker) {  
        		infowindow.setContent(parentDiv); 
        		infowindow.marker = marker;
        		infowindow.addListener('closeclick', function() {
        			infowindow.marker = null;
        		});
        		infowindow.open(map, marker);
        	}  
        }
        function getParentDiv(episodeId, episodeName, episodeDescription, timeTaken){
        	var index = 0;
        	var parentDiv = document.createElement('div');
        	parentDiv.id ="image-parentDiv";
        	parentDiv.className = "imageParentDiv";
        	var innerDiv = document.createElement('div');
        	innerDiv.id = "image-innerDiv";
        	innerDiv.className = "imageInnerDiv";


        	var leftTag = document.createElement('button');
        	leftTag.className ="left-tag";
        	leftTag.id ="lefttag";
        	leftTag.style = "position:absolute;top:45%;left:0";
        	leftTag.innerHTML = "❮";

        	var rightTag = document.createElement('button');
        	rightTag.className ="right-tag";
        	rightTag.id ="righttag";
        	rightTag.style = "position:absolute;top:45%;right:0";
        	rightTag.innerHTML = "❯"; 

        	var bottomDiv = document.createElement('div');
        	bottomDiv.id ="bottom-div";
        	bottomDiv.className = "bottomDiv";
        	bottomDiv.innerHTML = "<b>Episode Name: </b>" + episodeName
        	+ "<br><b>Episode Description: </b>" + episodeDescription
        	+ "<br><b>Time Taken: </b>" + timeTaken;

        	var image = document.createElement('img');
        	image.id = "imageInner"
        	image.width ="400";
        	
        	
        	var imagePaths = [];
        	$.getJSON('http://localhost:5000/photos/'+ episodeId +'/JSON', function(data){
        		for (var i = 0; i < data.photos.length;i++){
        			var imageName = data.photos[i].filename;
        			var imagePath = "http://localhost:5000/photo/" + episodeId + "/" + imageName;
        			imagePaths.push(imagePath);
        		}
        		
        		image.src = imagePaths[index];
        		
        		leftTag.onclick = function(){
        			if (index-1 >= 0 && index-1 < imagePaths.length){
        				index = index -1;
        			} else if (index-1 < 0){
        				index = imagePaths.length - 1;

        			} else{
        				index = 0;
        			}
        			image.src = imagePaths[index];
        		}; 

        		rightTag.onclick = function(){
        			if (index+1 >= 0 && index+1 < imagePaths.length){
        				index = index +1;
        			} else if (index+1 >= imagePaths.length){
        				index = 0;
        			} else{
        				index = imagePaths.length - 1;
        			}
        			image.src = imagePaths[index];
        		};  
        	});

        	innerDiv.appendChild(image);
        	parentDiv.appendChild(innerDiv); 
        	parentDiv.appendChild(leftTag); 
        	parentDiv.appendChild(rightTag); 
        	parentDiv.appendChild(bottomDiv);

        	return parentDiv;
        }

        function showListings() {
        	var bounds = new google.maps.LatLngBounds();
        	for (var i = 0; i < markers.length; i++) {
        		markers[i].setMap(map);
        		bounds.extend(markers[i].position);
        	}
        	map.fitBounds(bounds);
        }

        function hideListings() {
        	for (var i = 0; i < markers.length; i++) {
        		markers[i].setMap(null);
        	}
        }  

        function makeMarkerIcon(markerColor) {
        	var markerImage = new google.maps.MarkerImage(
        		'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor +
        		'|40|_|%E2%80%A2',
        		new google.maps.Size(21, 34),
        		new google.maps.Point(0, 0),
        		new google.maps.Point(10, 34),
        		new google.maps.Size(21,34));
        	return markerImage;
        }
        function toggleDrawing(drawingManager) {
        	if (drawingManager.map) {
        		drawingManager.setMap(null);
        		if (polygon !== null) {
        			polygon.setMap(null);
        		}
        	} else {
        		drawingManager.setMap(map);
        	}
        }
        
        function searchWithinPolygon() {
        	for (var i = 0; i < markers.length; i++) {
        		if (google.maps.geometry.poly.containsLocation(markers[i].position, polygon)) {
        			markers[i].setMap(map);
        		} else {
        			markers[i].setMap(null);
        		}
        	}
        }
        
        function zoomToEpisode(){
        	var searchTerm = document.getElementById("zoom-to-episode-text").value;
        	if (searchTerm === ''){
        		window.alert('You must enter an episode name');
        	} 
        	var foundEpisode = false;
        	var location;
        	var searchArray = searchTerm.split(" "); 
          //document.getElementById("test").innerHTML = markers.length;
          loop1:
          for (var i = 0; i < markers.length; i++){
          	if (markers[i].title.trim().toLowerCase() === searchTerm.trim().toLowerCase()){
          		foundEpisode = true;
          		location = markers[i].position;
          		break loop1;
          	} else {
          		loop2:
          		for (var j = 0; j < searchArray.length; j++){
          			if (markers[i].title.toLowerCase().includes(searchArray[j].toLowerCase())){
          				foundEpisode = true;
          				location = markers[i].position;
          				break loop1;
          			}
          		}
          	}
          } 

          if (foundEpisode == true){
          	map.setCenter(location);
          	map.setZoom(14);
          } else {
          	window.alert("Episode name not exist");
          }
        } 

        function zoomToArea() {
        	var geocoder = new google.maps.Geocoder(); 
        	var address = document.getElementById('zoom-to-area-text').value;
        	if (address == '') {
        		window.alert('You must enter an area, or address.');
        	} else {
        		geocoder.geocode(
        			{ address: address,
        			}, function(results, status) {
        				if (status == google.maps.GeocoderStatus.OK) {
        					map.setCenter(results[0].geometry.location);
        					map.setZoom(14);
        				} else {
        					window.alert('We could not find that location - try entering a more' +
        						' specific place.');
        				}
        			});
        	}   
        }
