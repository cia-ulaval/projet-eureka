<template>
    <div id="map"></div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
    name: 'LeafletMap',
    data() {
        return {
            roads: [
                {
                    coordinates: [
                        [0, -30],
                        [0, 30],
                        [10, 15],
                        [10, -15],
                        [0, -30]
                    ],
                    traffic: 0.7,
                    speedLimit: 50
                },
                {
                    coordinates: [
                        [10, 15],
                        [12, 17],
                        [10, 30]
                    ],
                    traffic: 0.1,
                    speedLimit: 30
                }

            ],
            intersections: [
                {
                    coordinates: [0, -30],
                    type: "trafficLight"
                },
                {
                    coordinates: [0, 30],
                    type: "stopSign"
                },
                {
                    coordinates: [10, 15],
                    type: "trafficLight"
                },
                {
                    coordinates: [10, -15],
                    type: "trafficLight"
                },
                {
                    coordinates: [10, 30],
                    type: "stopSign"
                }
            ],
            buildings: [
                {
                    vertices: [
                        [3, -5],
                        [8, -5],
                        [8, 5],
                        [3, 5],
                    ],
                    type: "school"
                },
                {
                    vertices: [
                        [5, -18],
                        [7, -15],
                        [8, -18],
                        [2, -25],
                        [2, -18],

                    ],
                    type: "parc"
                },
                {
                    vertices: [
                        [3, -28],
                        [8, -23],
                        [8, -28],
                    ],
                    type: "church"
                },
                {
                    vertices: [
                        [-7, 0],
                        [-2, 0],
                        [-2, 15],
                        [-7, 15],
                    ],
                    type: "shop"
                }
            ]
        }
    },
    mounted() {
        const map = L.map('map', { zoomControl: false }).setView([0, 0], 4);

        for (let i = 0; i < this.buildings.length; i++) {
            let buildingVertices = this.buildings[i].vertices;
            let buildingType = this.buildings[i].type;
            this.addBuildingToMap(map, buildingVertices, buildingType);
        }
        for(let i = 0; i < this.roads.length; i++){
            let roadCoordinate = this.roads[i].coordinates;
            this.addRoadToMap(map, roadCoordinate, this.roads[i].speedLimit);
        }
        for (let i = 0; i < this.roads.length; i++) {
            let roadCoordinate = this.roads[i].coordinates;
            let trafficIntensity = this.roads[i].traffic;
            this.addTrafficToMap(map, roadCoordinate, trafficIntensity);
        }
        for (let i = 0; i < this.intersections.length; i++) {
            let intersectionCoordinate = this.intersections[i].coordinates;
            let intersectionType = this.intersections[i].type;
            this.addIntersectionToMap(map, intersectionCoordinate, intersectionType);
        }
    },
    methods: {
        addRoadToMap(map, roadCoordinate, speedLimit) {
            let road = L.polyline(roadCoordinate, {
                color: 'black',
                weight: speedLimit/10*2+20,
                opacity: 1,
                // lineJoin: '',
                noClip: true
            });
            let markRoad = L.polyline(roadCoordinate, {
                color: 'yellow',
                weight: speedLimit/100+2,
                opacity: 1,
                dashArray: '20, 20',
                dashOffset: '20',
                noClip: true
            });

            road.addTo(map);
            markRoad.addTo(map);
        },
        addTrafficToMap(map, roadCoordinate, trafficIntensity) {
            const color = this.getColorGradient(trafficIntensity);
            let trafficIndicator = L.polyline(roadCoordinate, {
                color: `rgb(${color[0]}, ${color[1]}, ${color[2]})`,
                weight: 20,
                opacity: 0.6,
                lineJoin: 'round',
            })
            trafficIndicator.addTo(map)
        },
        getColorGradient(percentage) {
            const startColor = [0, 255, 0];
            const endColor = [255, 0, 0];
            const color = [];
            for (let i = 0; i < 3; i++) {
                color.push(Math.round((endColor[i] - startColor[i]) * percentage + startColor[i]));
            }
            return color;
        },
        addIntersectionToMap(map, intersectionCoordinate, intersectionType) {
            let iconFilePath = 'http://localhost:8080/intersectionIcons/'+intersectionType+'.png';
            console.log(intersectionType)
            let intersectionIcon = L.icon({
                iconUrl: iconFilePath,
                iconSize: [50, 50],
                iconAnchor: [25, 25],
                popupAnchor: [0, 0]
            });
            let intersectionMarker = L.marker(intersectionCoordinate, { icon: intersectionIcon });
            intersectionMarker.addTo(map);
        },
        addBuildingToMap(map, buildingVertices, buildingType) {
            let color = "rgb(209, 144, 48)"
            let fillColor = "rgb(184, 125, 44)"
            if (buildingType === "parc") {
                fillColor = "green"
                color = "green"
                this.addMarkerToMap(map, buildingVertices, buildingType)
            }
            else if (buildingType === "church") {
                fillColor = "rgb(134, 91, 31)"
                this.addMarkerToMap(map, buildingVertices, buildingType)
            }
            else if (buildingType === "shop") {
                fillColor = "rgb(42,124,196)"
                color = "rgb(34,102,159)"
                this.addMarkerToMap(map, buildingVertices, buildingType)
            }
            else if (buildingType === "school") {
                this.addMarkerToMap(map, buildingVertices, buildingType)
            }
            let building = L.polygon(buildingVertices, {
                color: color,
                weight: 1,
                opacity: 1,
                fillColor: fillColor,
                fillOpacity: 1,
                noClip: true
            });
            building.addTo(map);
        },
        addMarkerToMap (map, buildingVertices, buildingType) {
            let iconFilePath = 'http://localhost:8080/buildingIcons/'+buildingType+'.png';
            let buildingIcon = L.icon({
                iconUrl: iconFilePath,
                iconSize: [20, 20],
                iconAnchor: [10, 10],
                popupAnchor: [0, 0]
            });
            let center = this.getCenterFromVertices(buildingVertices);
            let buildingMarker = L.marker(center, { icon: buildingIcon });
            buildingMarker.addTo(map);
        },
        getCenterFromVertices (vertices) {
            let center = [0, 0];
            for (let i = 0; i < vertices.length; i++) {
                center[0] += vertices[i][0];
                center[1] += vertices[i][1];
            }
            center[0] /= vertices.length;
            center[1] /= vertices.length;
            return center;
        },

    },

};
</script>

<style>
#map {
    height: 500px;
}
.leaflet-container {
    background-color:rgba(255,0,0,0.0);
}
</style>
