// style from: https://snazzymaps.com/style/61/blue-essence
var map_style = [{"featureType": "landscape.natural", "elementType": "geometry.fill", "stylers": [{"visibility": "on"}, {"color": "#e0efef"} ] }, {"featureType": "poi", "elementType": "geometry.fill", "stylers": [{"visibility": "on"}, {"hue": "#1900ff"}, {"color": "#c0e8e8"} ] }, {"featureType": "road", "elementType": "geometry", "stylers": [{"lightness": 100 }, {"visibility": "simplified"} ] }, {"featureType": "road", "elementType": "labels", "stylers": [{"visibility": "off"} ] }, {"featureType": "transit.line", "elementType": "geometry", "stylers": [{"visibility": "on"}, {"lightness": 700 } ] }, {"featureType": "water", "elementType": "all", "stylers": [{"color": "#7dcdcd"} ] } ]
// load gMaps
function initMap() {
	var coord = {lat: 43.646254, lng: -79.384212};

	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 15,
		center: coord
	});

	map.set('styles', map_style);
}

	//{% load static %}
	//map.data.loadGeoJson("{% static "maps/toronto_selection.geojson" %}")