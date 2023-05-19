<script setup>
import {useFBX} from '@tresjs/cientos'
import {shallowRef} from "vue";
import {useRenderLoop} from "@tresjs/core";

// const CUBE_SIZE = 400

const model = await useFBX('/models/Car.fbx')

// const tensorFile = require('../data/tensor.json')

const boxRef = shallowRef(null)
const intersectionRef = shallowRef(null)

const {onLoop} = useRenderLoop()

let carPosition = [0, 0]
let carOrientation = "up"

function moveMap(delta) {
    let dx = 0
    let dy = 0
    switch (carOrientation) {
        case "up":
            dy = 1
            break;
        case "down":
            dy = -1
            break;
        case "left":
            dx = 1
            break;
        case "right":
            dx = -1
            break;
    }

    let distance = 1000*delta

    for (let i = 0; i < boxRef.value.length; i++) {
        let cube = boxRef.value[i];
        cube.position.z -= dy*distance
        cube.position.x -= dx*distance
    }
    for (let i = 0; i < intersectionRef.value.length; i++) {
        let cube = intersectionRef.value[i];
        cube.position.z -= dy*distance;
        cube.position.x -= dx*distance;
    }
    carPosition[0] += dx*distance
    carPosition[1] += dy*distance
}

function isNextCubeAnIntersection() {
    // according to the car position and orientation and the tensor, check if the next cube is an intersection, i.e one of the 3 values is 1
    // if it is, return true, else return false
    let row = Math.round(carPosition[0] / CUBE_SIZE);
    let col = Math.round(carPosition[1] / CUBE_SIZE);

    switch (carOrientation) {
        case "up":
            return tensor[row][col + 1] === 1 || tensor[row][col - 1] === 1 || tensor[row - 1][col] === 1;
        case "down":
            return tensor[row][col + 1] === 1 || tensor[row][col - 1] === 1 || tensor[row + 1][col] === 1;
        case "left":
            return tensor[row][col - 1] === 1 || tensor[row + 1][col] === 1 || tensor[row - 1][col] === 1;
        case "right":
            return tensor[row][col + 1] === 1 || tensor[row + 1][col] === 1 || tensor[row - 1][col] === 1;
    }
}

onLoop(({delta}) => {
    if (boxRef.value) {
        if (isNextCubeAnIntersection()) {
            if(nextDirection !== null) {
                carOrientation = nextDirection
                moveMap(delta)
                console.log(carOrientation)
            }
        }
        else {
            nextDirection = null
            moveMap(delta)
            console.log(carOrientation)
        }
    }
})
</script>
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
            <TresPerspectiveCamera :position="[0, 300, -800]" :look-at="mapCenter" :far="100000"/>
        <OrbitControls/>
            <TresScene>
                <TresMesh v-for="(cube, index) in map" :key="index" :position="cube.position" ref="boxRef">
                    <TresBoxGeometry :args="cube.dimensions"/>
                    <TresMeshBasicMaterial :color="cube.color"/>
                </TresMesh>
                <TresMesh v-for="(cube, index) in intersection" :key="index" :position="cube.position" ref="intersectionRef">
                    <TresBoxGeometry :args="cube.dimensions"/>
                    <TresMeshBasicMaterial :color="cube.color"/>
                </TresMesh>
            <Suspense>
                <TresMesh v-bind="model"/>
            </Suspense>
        </TresScene>
            <TresAmbientLight/>
        map.length/2
        </TresCanvas>
    </div>
</template>

<script>
import {TresCanvas} from '@tresjs/core'
import {OrbitControls} from "@tresjs/cientos";

const CUBE_SIZE = 400
const CAR_SIZE = 200

let nextDirection = null
console.log(nextDirection)

import tensor from '../data/tensor.json'
import speedTensor from '../data/speedTensor.json'
import stopTensor from '../data/stopTensor.json'
export default {
    name: 'ThreeCanvas',
    components: {
        OrbitControls: OrbitControls,
        TresCanvas: TresCanvas,
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
        }
    },
    methods: {
        move(direction){
            switch (direction) {
                case 'up':
                    nextDirection = 'up'
                    break;
                case 'left':
                    nextDirection = 'left'
                    break;
                case 'right':
                    nextDirection = 'right'
                    break;
                case 'down':
                    nextDirection = 'down'
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
                    if (this.tensor[i][j] === 1) map.push({position: [i*CUBE_SIZE, -CAR_SIZE, j*CUBE_SIZE], color: 'black', dimensions: [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE]})
                    if (this.tensor[i][j] === 0) map.push({position: [i*CUBE_SIZE, -CAR_SIZE, j*CUBE_SIZE], color: '#41980A', dimensions: [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE]})
                }
            }
            this.map = map
        },
        tensorToIntersection() {
            let intersection = []
            for (let i = 0; i < this.stopTensor.length; i++) {
                for (let j = 0; j < this.stopTensor[i].length; j++) {
                    if (this.stopTensor[i][j] === 1) intersection.push({position: [i*CUBE_SIZE, CUBE_SIZE-CAR_SIZE, j*CUBE_SIZE], color: 'red', dimensions: [0.3*CUBE_SIZE, 0.3*CUBE_SIZE, 0.3*CUBE_SIZE]})
                    if (this.stopTensor[i][j] === 2) intersection.push({position: [i*CUBE_SIZE, CUBE_SIZE-CAR_SIZE, j*CUBE_SIZE], color: 'blue', dimensions: [0.3*CUBE_SIZE, 0.3*CUBE_SIZE, 0.3*CUBE_SIZE]})
                }
            }
            this.intersection = intersection
        },
    },
    mounted() {
        this.tensorToMap();
        this.tensorToIntersection();
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
