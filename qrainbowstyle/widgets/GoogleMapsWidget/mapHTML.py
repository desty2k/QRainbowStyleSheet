html = """
<!DOCTYPE html>
<html>
<head>
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <style>
        #map {
            height: 100%;
        }

        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
    </style>
</head>
<body>
<div id="map"></div>
<script>

    var jshelper;

    new QWebChannel(qt.webChannelTransport,
                function(channel) { jshelper = channel.objects.jshelper; });

    var customStyle = [
        {
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "COLOR_BACKGROUND_DARK"
                }
            ]
        },
        {
            "featureType": "landscape",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "COLOR_BACKGROUND_LIGHT"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#29768a"
                },
                {
                    "lightness": -37
                }
            ]
        },
        {
            "featureType": "poi",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#406d80"
                }
            ]
        },
        {
            "featureType": "transit",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#406d80"
                }
            ]
        },
        {
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "visibility": "on"
                },
                {
                    "color": "COLOR_SELECTION_LIGHT"
                },
                {
                    "weight": 2
                },
                {
                    "gamma": 0.84
                }
            ]
        },
        {
            "elementType": "labels.text.fill",
            "stylers": [
                {
                    "color": "COLOR_FOREGROUND_LIGHT"
                }
            ]
        },
        {
            "featureType": "administrative",
            "elementType": "geometry",
            "stylers": [
                {
                    "weight": 0.6
                },
                {
                    "color": "#1a3541"
                }
            ]
        },
        {
            "elementType": "labels.icon",
            "stylers": [
                {
                    "visibility": "off"
                }
            ]
        },
        {
            "featureType": "poi.park",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "#2c5a71"
                }
            ]
        }
    ]

    function initMap() {

        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 3,
            center: {lat: 0, lng: -180},
            disableDefaultUI: true,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            styles: customStyle,
            restriction: {
                latLngBounds: {
                    north: 85.0,
                    south: -85.0,
                    west: -179.9999,
                    east: 179.9999
                },
                strictBounds: true
            }
        });
        map.setOptions({minZoom: 0, maxZoom: 50});

        /*
        var flightPlanCoordinates = [
            new google.maps.LatLng(53.08254, 19.37103),
            new google.maps.LatLng(58.46758, 110.027892)
          ];
        var flightPath = new google.maps.Polyline({
            path: flightPlanCoordinates,
            strokeColor: "#ff1e00",
            strokeOpacity: 1.0,
            strokeWeight: 2
        });
        flightPath.setMap(map);
        */

        google.maps.event.addListener(map, "rightclick", function(event) {
            var lat = event.latLng.lat();
            var lng = event.latLng.lng();
            jshelper.logLocation(lat, lng)
        });
    }


</script>
<script async defer
        src="https://maps.googleapis.com/maps/api/js?key=API_KEY_GOES_HERE&callback=initMap">
</script>
</body>
</html>
"""
