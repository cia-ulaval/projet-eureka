<template>
    <div class="container">
        <div class="gamePad">
            <br>
            <button class="arrows" @click="move('up')"><img src="../assets/arrow.svg" class="up"></button>
            <br>
            <button class="arrows" @click="move('left')"><img src="../assets/arrow.svg" class="left"></button>
            <button class="arrows" @click="move('down')"><img src="../assets/arrow.svg" class="down"></button>
            <button class="arrows" @click="move('right')"><img src="../assets/arrow.svg" class="right"></button>
        </div>
        <TresCanvas clear-color="#82DBC5" window-size="true" class="canvas">
            <TresPerspectiveCamera :position="[25, 15, 25]" :look-at="mapCenter"/>
            <TresScene>
                <TresMesh v-for="(cube, index) in map" :key="index" :position="cube.position">
                    <TresBoxGeometry :args="cube.dimensions"/>
                    <TresMeshBasicMaterial :color="cube.color"/>
                </TresMesh>
                <TresMesh v-for="(cube, index) in intersection" :key="index" :position="cube.position">
                    <TresBoxGeometry :args="cube.dimensions"/>
                    <TresMeshBasicMaterial :color="cube.color"/>
                </TresMesh>
                <TresMesh v-bind="carPosition">
                    <TresBoxGeometry :args="car.dimensions"/>
                    <TresMeshBasicMaterial :color="car.color"/>
                </TresMesh>
            </TresScene>
            <TresAmbientLight/>map.length/2
        </TresCanvas>
    </div>
</template>

<script>
import {TresCanvas, useRenderLoop } from '@tresjs/core'
import {shallowRef} from 'vue'

import tensor from '../data/tensor.json'
import speedTensor from '../data/speedTensor.json'
import stopTensor from '../data/stopTensor.json'
import { getMap } from '@/js/map.js'

export default {
    name: 'ThreeCanvas',
    components:{
        TresCanvas: TresCanvas,
    },
    setup: function () {

        const { onLoop } = useRenderLoop()

        const boxRef = shallowRef(null)


        onLoop(() => {
            if(boxRef.value){
                console.log(boxRef.value.position)
            }
        })
    },
    data(){
        return{
            mapCenter: [15, 1, 13],
            car: {
                position: [15, 1, 13],
                color: 'orange',
                dimensions: [0.5, 0.5, 0.5]
            },
            map: [],
            intersection: [],
            tensor: tensor,
            speedTensor: speedTensor,
            stopTensor: stopTensor,
            trafficTensor : [],
            start : [],
            end : []
        }
    },
    computed: {
        carPosition(){
            return this.car
        }
    },
    methods: {
        move(direction){
            switch (direction) {
                case 'up':
                    this.car.position[0] -= 1;
                    console.log(this.car.position)
                    break;
                case 'left':
                    // Code to move left
                    break;
                case 'right':
                    // Code to move right
                    break;
                case 'down':
                    // Code to move down
                    break;
                default:
                    break;
            }
        },
        findNextIntersection(){
            const row = this.car.position[0];
            const col = this.car.position[2];
            const intersections = this.intersection;
            const map = this.tensor;

            // Check left intersection
            if (col > 0 && map[row][col - 1] === 2) {
                intersections.push([row, col - 1]);
            }

            // Check right intersection
            if (col < map[row].length - 1 && map[row][col + 1] === 2) {
                intersections.push([row, col + 1]);
            }

            // Check up intersection
            if (row > 0 && map[row - 1][col] === 2) {
                intersections.push([row - 1, col]);
            }

            // Check down intersection
            if (row < map.length - 1 && map[row + 1][col] === 2) {
                intersections.push([row + 1, col]);
            }

            return intersections;
        },
        tensorToMap() {
            let map = []
            for (let i = 0; i < this.tensor.length; i++) {
                for (let j = 0; j < this.tensor[i].length; j++) {
                    if (this.tensor[i][j] === 1) map.push({position: [i, 0, j], color: 'black', dimensions: [1, 1, 1]})
                    if (this.tensor[i][j] === 0) map.push({position: [i, 0, j], color: '#41980A', dimensions: [1, 1, 1]})

                }
            }
            this.map = map
        },
        tensorToIntersection() {
            let intersection = []
            for (let i = 0; i < this.stopTensor.length; i++) {
                for (let j = 0; j < this.stopTensor[i].length; j++) {
                    if (this.stopTensor[i][j] === 1) intersection.push({position: [i, 1, j], color: 'red', dimensions: [0.3, 0.3, 0.3]})
                    if (this.stopTensor[i][j] === 2) intersection.push({position: [i, 1, j], color: 'blue', dimensions: [0.3, 0.3, 0.3]})
                }
            }
            this.intersection = intersection
        },
        async fetchMap() {
          const mapInfos = await getMap();
          this.start = mapInfos.start;
          this.end = mapInfos.end;
          this.trafficTensor = mapInfos.traffic;
      }
    },
    mounted() {
        this.tensorToIntersection();
        this.tensorToMap();
        this.fetchMap();
    }

}
</script>

<style scoped>
img {
    filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(354deg) brightness(102%) contrast(101%);
}
.container{
    position: relative;
    left: 0;
    top: 0;
}
.canvas {
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;
    z-index: 1;
}
.arrows {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100px;
    height: 100px;
    background-color: rgba(2,0,36,0.3);
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 24px;
    font-weight: bold;
    cursor: pointer;
}
.gamePad {
    transform: rotate(-55deg);
    position: absolute;
    left: 770px;
    top: 500px;
    z-index: 2;
    display: grid;
    grid-template-columns: 120px 120px 120px;
    grid-template-rows: 120px 120px;
    gap: 0px 0px;
    grid-template-areas:
    ". up ."
    "left down right";
}
.up {
    grid-area: up;
}
.left {
    transform: rotate(-90deg);
    grid-area: left;
}
.down {
    transform: rotate(180deg);
    grid-area: down;
}
.right {
    transform: rotate(90deg);
    grid-area: right;
}
</style>
