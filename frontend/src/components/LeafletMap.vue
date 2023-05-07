<template>
    <div id="map"></div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
    name: 'LeafletMap',
    mounted() {
        const map = L.map('map').setView([0, 0], 4);

        const roadCoordinates = [
            [0, -30],
            [0, 30],
            [10, 15],
            [10, -15],
            [0, -30]
        ];

// Create a polyline to represent the road
        const road = L.polyline(roadCoordinates, {
            color: 'black',
            weight: 25,
            opacity: 0.7,
            lineJoin: 'round',
            noClip: true
        });
        const markRoad = L.polyline(roadCoordinates, {
            color: 'yellow',
            weight: 2,
            opacity: 0.7,
            dashArray: '20, 20',
            dashOffset: '20',
            noClip: true
        });


// Add the road to the map
        road.addTo(map);
        markRoad.addTo(map);
        // markTrafficRoad.addTo(map);

        map.on('zoomend', function() {
            var zoomLevel = map.getZoom();
            var weight = 10 * Math.abs(zoomLevel);

            // Set the width of the road
            road.setStyle({
                weight: weight,
                stroke: true,
                fill: false
            });
        });
    },
};
</script>

<style>
#map {
    height: 500px;
}
</style>
