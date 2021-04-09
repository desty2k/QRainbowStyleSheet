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

<script async>

    var jshelper;
    new QWebChannel(qt.webChannelTransport,
                function(channel) { jshelper = channel.objects.jshelper; });
    let map;
    let markers = {};
    let polylines = {};
    let allow_marker_dragging = true;
    let map_draggable = true;
    let map_zoomControl = false;
    let map_scrollwheel = true;
    let map_disableDoubleClickZoom = false;

    window.addEventListener('load', (event) => {
        jshelper.pageIsLoaded();
    });

    window.addEventListener('resize', (event) => {
        jshelper.pageIsResized();
    });

    const image = "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png";
    var customStyle = [
        {
            "featureType": "water",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "COLOR_BACKGROUND_1"
                }
            ]
        },
        {
            "featureType": "landscape",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "COLOR_BACKGROUND_5"
                }
            ]
        },
        {
            "featureType": "road",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "COLOR_BACKGROUND_3"
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
                    "color": "COLOR_BACKGROUND_3"
                }
            ]
        },
        {
            "featureType": "transit",
            "elementType": "geometry",
            "stylers": [
                {
                    "color": "COLOR_BACKGROUND_3"
                }
            ]
        },
        {
            "elementType": "labels.text.stroke",
            "stylers": [
                {
                    "visibility": "off"
                },
                {
                    "color": "COLOR_ACCENT_4"
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
                    "color": "COLOR_TEXT_1"
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
    ]

    function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 0,
            center: {lat: 50, lng: 0},
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
        map.setOptions({minZoom: 0, maxZoom: 50, draggable: map_draggable, zoomControl: map_zoomControl, scrollwheel: map_scrollwheel, disableDoubleClickZoom: map_disableDoubleClickZoom});

        google.maps.event.addListener(map, "rightclick", function (event) {
            jshelper.mapIsRightClicked(event.latLng.lat(), event.latLng.lng())
        });

        google.maps.event.addListener(map, 'dragend', function () {
            var center = map.getCenter();
            jshelper.mapIsMoved(center.lat(), center.lng());
        });

        google.maps.event.addListener(map, 'click', function (event) {
            jshelper.mapIsClicked(event.latLng.lat(), event.latLng.lng());
        });

        google.maps.event.addListener(map, 'dblclick', function (event) {
            jshelper.mapIsDoubleClicked(event.latLng.lat(), event.latLng.lng());
        });

        google.maps.event.addListenerOnce(map, 'idle', function (){
            jshelper.mapIsFullyLoaded();
        });

        google.maps.event.addListener(map, 'tilesloaded', function () {
            jshelper.tilesAreFullyLoaded();
        });

        console.log("Setup compeleted!");
    }


function addMarker(marker_id, latitude, longitude, params) {
    console.log("Creating new marker: " + marker_id)
    const location = new google.maps.LatLng(latitude, longitude);

    if (marker_id in markers) {
        return updateMarker(marker_id, {position:location})
    }

    const marker = new google.maps.Marker(Object.assign({},
        {position: location,
        map: map,
        draggable: allow_marker_dragging,
        id: marker_id,
        polylines: []},
        params));

    google.maps.event.addListener(marker, 'click', function () {
        jshelper.markerIsClicked(marker_id, marker.position.lat(), marker.position.lng())
    });
    google.maps.event.addListener(marker, 'dblclick', function () {
        jshelper.markerIsDoubleClicked(marker_id, marker.position.lat(), marker.position.lng())
    });
    google.maps.event.addListener(marker, 'rightclick', function () {
         jshelper.markerIsRightClicked(marker_id, marker.position.lat(), marker.position.lng())
    });
    google.maps.event.addListener(marker, 'dragend', function () {
         jshelper.markerIsMoved(marker_id, marker.position.lat(), marker.position.lng())
    });
    markers[marker_id] = marker;
}

function addPolyline(polyline_id, coordsArray) {
    console.log("Creating new polyline: " + polyline_id)
    for (var i = 0; i < coordsArray.length; i++) {
        coordsArray[i]["lat"] = parseFloat(coordsArray[i]["lat"]);
        coordsArray[i]["lng"] = parseFloat(coordsArray[i]["lng"]);
    }

    const connection = new google.maps.Polyline({
        path: coordsArray,
        geodesic: true,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2,
        map: map,
        markers: [],
    });

    google.maps.event.addListener(connection, 'click', function () {
        jshelper.polylineIsClicked(polyline_id, connection.getPath().getArray())
    });
    google.maps.event.addListener(connection, 'dblclick', function () {
        jshelper.polylineIsDoubleClicked(polyline_id, connection.getPath().getArray())
    });
    google.maps.event.addListener(connection, 'rightclick', function () {
         jshelper.polylineIsRightClicked(polyline_id, connection.getPath().getArray())
    });
    polylines[polyline_id] = connection;
}

function addPolylineBetweenMarkers(polyline_id, markersArray) {
    let cordsArray = [];
    for (let marker_id in markersArray) {
        cordsArray.push(markers[marker_id].getPosition());
    }
    addPolyline(polyline_id, cordsArray)
}

function deletePolyline(polyline_id) {
    polylines[polyline_id].setMap(null);
    delete polylines[polyline_id];
}

function getMarkers() {
    let resp = {};
    for (var mid in markers) {
        resp[mid] = {lat: markers[mid].position.lat(), lng: markers[mid].position.lng()};
    }
    return resp;
}

function moveMarker(marker_id, latitude, longitude) {
    let cords = new google.maps.LatLng(latitude, longitude);
    markers[marker_id].setPosition(cords);
}

function deleteMarker(marker_id) {
    markers[marker_id].setMap(null);
    delete markers[marker_id];
}

function updateMarker(marker_id, extras) {
    if (!(marker_id in markers)) {
        return;
    }
    markers[marker_id].setOptions(extras);
}

function enableMarkersDragging(value) {
    allow_marker_dragging = value;
    for (var marker_id in markers) {
        updateMarker(marker_id, {draggable: value});
    }
}

function disableMapDragging(value) {
    map_draggable = value;
    map.setOptions({draggable: value});
}

function showZoomControl(value) {
    map_zoomControl = value;
    map.setOptions({zoomControl: value});
}

function disableScrollWheel(value) {
    map_scrollwheel = value;
    map.setOptions({scrollwheel: value});
}

function disableDoubleClickToZoom(value) {
    map_disableDoubleClickZoom = value;
    map.setOptions({disableDoubleClickZoom: value});
}

function panToCenter() {
    map.panTo(map.getCenter());
}

</script>
<script async
        src="https://maps.googleapis.com/maps/api/js?key=API_KEY_GOES_HERE&callback=initMap">
</script>
</body>
</html>
"""
