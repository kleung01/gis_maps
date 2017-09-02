function initMap() {
  var uluru = {lat: 43.6567919, lng: -79.4609311};

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: uluru
  });
}