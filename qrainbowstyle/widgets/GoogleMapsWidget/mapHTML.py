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

    
    window.addEventListener('load', (event) => {
        console.log('Page is fully loaded!');
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
        map = new google.maps.Map(document.getElementById('map'), {
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


function addMarker(marker_id, latitude, longitude) {
    console.log("Creating new marker: " + marker_id)
    const location = new google.maps.LatLng(latitude, longitude);

    if (marker_id in markers) {
        return updateMarker(marker_id, {position:location})
    }

    const marker = new google.maps.Marker({
        position: location,
        map: map,
        draggable: allow_marker_dragging,
        id: marker_id,
        polylines: {},
    });

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
        const connection = new google.maps.Polyline({
        path: coordsArray,
        geodesic: true,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2,
        map: map,
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

function getMarkers() {
    let resp = {};
    for (var mid in markers) {
        resp[mid] = {lat: markers[mid].position.lat(), lng: markers[mid].position.lng()};
    }
    return resp;
}

function moveMarker(marker_id, latitude, longitude) {
    /*
    var newcords = new google.maps.LatLng(latitude, longitude);
    for (var poly_id in polylines) {
        if (polylines[poly_id].get("markers").length > 0) {
            if(marker_id in polylines[poly_id].get("markers")) {
                var oldcords = polylines[poly_id].getPath().getArray();
                oldcords[marker_id] = newcords;
                polylines[poly_id].setPath(oldcords);
            }
        }
    }
    */
}

function deleteMarker(marker_id) {
    markers[marker_id].setMap(null);
    delete markers[marker_id];
    /*
    for (var poly_id in polylines) {
        if (polylines[poly_id].get("markers").length > 0) {
            if(marker_id in polylines[poly_id].get("markers")) {
                var oldcords = polylines[poly_id].getPath().getArray();
                oldcords.splice(marker_id, 1);
                polylines[poly_id]["markers"].splice(marker_id, 1);
                console.log("Removed marker with id: " + marker_id + "- New markersIDs for this poly: " + polylines[poly_id]["markers"])
                polylines[poly_id].setPath(oldcords);
            }
        }
    }
    */
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
    console.log("Dragging settings changed!")
}

</script>
<script async
        src="https://maps.googleapis.com/maps/api/js?key=API_KEY_GOES_HERE&callback=initMap">
</script>
</body>
</html>
"""
