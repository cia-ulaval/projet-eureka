<script setup>
import {useFBX} from '@tresjs/cientos'
import {shallowRef} from "vue";

const CAR_SCALE = 0.07

const model = await useFBX('/models/scene.fbx')

let carPos = [20, 0, 20]
let carRot = [67.5, 0, 67.5]
const carRef = shallowRef()
const car = model
car.position.set(carPos[0], 0, carPos[2])
car.rotation.set(carRot[0], carRot[1], carRot[2])
car.scale.set(CAR_SCALE, CAR_SCALE, CAR_SCALE)
car.updateMatrixWorld()

const handleMove = (direction) => {
    switch (direction) {
        case 'up':
            carPos[0] -= 1
            carRot = [67.5, 0, 67.5]
            moveCar()
            break;
        case 'left':
            carPos[2] += 1
            carRot = [67.5, 0, 0]
            moveCar()
            break;
        case 'right':
            carPos[2] -= 1
            carRot = [67.5, 0, 135]
            moveCar()
            break;
        case 'down':
            carPos[0] += 1
            carRot = [67.5, 0, 202.6]
            moveCar()
            break;
        default:
            break;
    }
}

function moveCar(){
    car.position.set(carPos[0], 0, carPos[2])
    car.rotation.set(carRot[0], carRot[1], carRot[2])
    car.updateMatrixWorld()
}
</script>
<template>
    <div class="container">
        <div class="gamePad">
            <br>
            <button class="arrows" @click="handleMove('up')"><img src="../assets/arrow.svg" class="up"></button>
            <br>
            <button class="arrows" @click="handleMove('left')"><img src="../assets/arrow.svg" class="left"></button>
            <button class="arrows" @click="handleMove('down')"><img src="../assets/arrow.svg" class="down"></button>
            <button class="arrows" @click="handleMove('right')"><img src="../assets/arrow.svg" class="right"></button>
        </div>
        <TresCanvas clear-color="#82DBC5" window-size="true" class="canvas">
            <TresPerspectiveCamera :position="[25, 15, 25]" :look-at="mapCenter"/>
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
                <TresMesh v-bind="car" ref="carRef"/>
            </Suspense>
        </TresScene>
            <TresAmbientLight :color="0x484068" :intensity="40" />
        map.length/2
        </TresCanvas>
    </div>
</template>

<script>
import {TresCanvas} from '@tresjs/core'

let nextDirection = null
console.log(nextDirection)

import tensor from '../data/tensor.json'
import speedTensor from '../data/speedTensor.json'
import stopTensor from '../data/stopTensor.json'
export default {
    name: 'ThreeCanvas',
    components: {
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
                    if (this.tensor[i][j] === 1) map.push({position: [i, -1, j], color: 'black', dimensions: [1, 1, 1]})
                    if (this.tensor[i][j] === 0) map.push({position: [i, -1, j], color: '#41980A', dimensions: [1, 1, 1]})
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
