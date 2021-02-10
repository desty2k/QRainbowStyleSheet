html = """
<!doctype html>
<html lang="en">

  <head>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/openlayers/openlayers.github.io@master/en/v6.5.0/css/ol.css" type="text/css">
    <style>
        .map {
            height: 100%;
        }

        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
        }
    </style>
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/openlayers/openlayers.github.io@master/en/v6.5.0/build/ol.js"></script>
    <title>OpenLayers example</title>
  </head>

  <body>
    <div id="map" class="map"></div>

    <script type="text/javascript" async>
        let jshelper;
        let map;
        let view;
        let markers = [];

        new QWebChannel(qt.webChannelTransport,
                function(channel) { jshelper = channel.objects.jshelper; });
        var vectorSource = new ol.source.Vector({
            features: markers
        });
        var vectorLayer = new ol.layer.Vector({
            source: vectorSource,
        });

        function initMap() {
            view = new ol.View({
                center: ol.proj.fromLonLat([0, 45]),
                zoom: 0,
                projection: "EPSG:3857",
                extent: ol.proj.get("EPSG:3857").getExtent(),
            });

            map = new ol.Map({
                target: 'map',
                layers: [
                    new ol.layer.Tile({
                        source: new ol.source.OSM()
                    })
                ],
                view: view,
            });
            map.addLayer(vectorLayer);
        }

        function addMarker(marker_id, longitude, latitude, params) {
            var iconGeometry=new ol.geom.Point(ol.proj.transform([latitude, longitude], 'EPSG:4326', 'EPSG:3857'))
            var iconFeature = new ol.Feature({
                geometry:iconGeometry
            });
            iconFeature.setId(marker_id)
            vectorSource.addFeature(iconFeature);
        }

    </script>

    <script async>
        initMap()
    </script>
  </body>
</html>
"""
