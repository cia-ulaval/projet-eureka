<script setup>
import {useFBX} from '@tresjs/cientos'
import {shallowRef} from "vue";
import {useRenderLoop, useTexture} from "@tresjs/core";
import ResultModal from "@/components/ResultModal.vue";


const upDownTexture = await useTexture({
    map: '/textures/upDown.jpg'
});
const leftRightTexture = await useTexture({
    map: '/textures/leftRight.jpg'
});
const otherTexture = await useTexture({
    map: '/textures/otherIntersection.jpg'
});
const grassTexture = await useTexture({
    map: '/textures/grass.jpg'
});


const model = await useFBX('/models/Car.fbx')

const boxRef = shallowRef(null)
const intersectionRef = shallowRef(null)

const {onLoop} = useRenderLoop()

let carPosition = null
let carOrientation = "up"

function moveMap(delta) {
    const rowCol = getTensorPosition()
    const row = rowCol[0]
    const col = rowCol[1]

    const speed = speedTensor[row][col] ** 2 / 5

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

    let distance = speed * delta

    for (let i = 0; i < boxRef.value.length; i++) {
        let cube = boxRef.value[i];
        cube.position.z -= dy * distance
        cube.position.x -= dx * distance
    }
    for (let i = 0; i < intersectionRef.value.length; i++) {
        let cube = intersectionRef.value[i];
        cube.position.z -= dy * distance;
        cube.position.x -= dx * distance;
    }
    carPosition[0] += dx * distance
    carPosition[1] += dy * distance
    return distance
}

function isNextCubeAnIntersection() {
    // according to the car position and orientation and the tensor, check if the next cube is an intersection, i.e one of the 3 values is 1
    // if it is, return true, else return false
    let rowCol = getTensorPosition()
    let row = rowCol[0]
    let col = rowCol[1]

    switch (carOrientation) {
        case "up":
            if (row === 0) {
                if (tensor[row + 1] === undefined) {
                    return false;
                }
                return tensor[row + 1][col] === 1;
            }
            if (tensor[row + 1] === undefined) {
                return tensor[row - 1][col] === 1;
            }
            return tensor[row + 1][col] === 1 || tensor[row - 1][col] === 1;
        case "down":
            if (row === 0) {
                if (tensor[row + 1] === undefined) {
                    return false;
                }
                return tensor[row + 1][col] === 1;
            }
            if (tensor[row + 1] === undefined) {
                return tensor[row - 1][col] === 1;
            }
            return tensor[row + 1][col] === 1 || tensor[row - 1][col] === 1;
        case "left":
            if (col === 0) {
                return tensor[row][col + 1] === 1;
            }
            return tensor[row][col + 1] === 1 || tensor[row][col - 1] === 1;
        case "right":
            if (col === 0) {
                return tensor[row][col + 1] === 1;
            }
            return tensor[row][col + 1] === 1 || tensor[row][col - 1] === 1;
    }
}

function getAvailableTurns() {
    // according to the car position and orientation and the tensor, return the available turns
    // if there is no turn, return null
    let rowCol = getTensorPosition()
    let row = rowCol[0]
    let col = rowCol[1]

    let turns = []

    if (col !== 0) {
        if (tensor[row][col - 1] === 1) {
            turns.push("down")
        }
    }
    if (tensor[row][col + 1] !== undefined) {
        if (tensor[row][col + 1] === 1) {
            turns.push("up")
        }
    }
    if (row !== 0) {
        if (tensor[row - 1][col] === 1) {
            turns.push("right")
        }
    }
    if (tensor[row + 1] !== undefined) {
        if (tensor[row + 1][col] === 1) {
            turns.push("left")
        }
    }

    return turns
}

function setCarOrientation(newOrientation) {
    carOrientation = newOrientation
    switch (newOrientation) {
        case "up":
            model.rotation.y = 0
            break;
        case "down":
            model.rotation.y = Math.PI
            break;
        case "left":
            model.rotation.y = Math.PI / 2
            break;
        case "right":
            model.rotation.y = -Math.PI / 2
            break;
    }
    model.updateWorldMatrix(true, true)
}

function getTensorPosition() {
    let row = Math.round(carPosition[0] / CUBE_SIZE);
    let col = Math.round(carPosition[1] / CUBE_SIZE);
    return [row, col]
}

function getRealWorldCoordinates(tensorPosition) {
    let row = tensorPosition[0]
    let col = tensorPosition[1]

    let x = row * CUBE_SIZE
    let z = col * CUBE_SIZE

    return [x, z]
}

let state = "moving"
let cubeToCross = null
let toDirection = null
let distanceToCross = null
let path = []

function addToPositionPath() {
    let tensorPosition = getTensorPosition()
    if (path.length === 0) {
        path.push(tensorPosition)
    } else {
        let last = path[path.length - 1]
        if (last[0] !== tensorPosition[0] || last[1] !== tensorPosition[1]) {
            path.push(tensorPosition)
        }
    }
}

function isTheEndReached() {
    const rowCol = getTensorPosition()
    const row = rowCol[0]
    const col = rowCol[1]

    return row === END[0] && col === END[1]

}

onLoop(({delta}) => {
    if(getShowModal()){
        return
    }
    if (START !== null && carPosition === null) {
        carPosition = getRealWorldCoordinates(START)
    }
    else{
        console.log("state=" + state + " - toDirection=" + toDirection + " - carOrientation=" + carOrientation + ' - distanceToCross='+distanceToCross + " - showModal="+ getShowModal())
        if (boxRef.value) {
            if (isTheEndReached() && getShowModal() === false) {
                carPosition = null
                setCarOrientation("up")
                setShowModal(true)
                return
            }
            switch (state) {
                case "moving":
                    if (isNextCubeAnIntersection()) {
                        state = "stopped"
                        cubeToCross = getTensorPosition()
                        nextDirection = null
                        break;
                    } else {
                        moveMap(delta)
                        break;
                    }
                case "stopped":
                    if (nextDirection !== null && getAvailableTurns().includes(nextDirection)) {
                        state = "crossing"
                        toDirection = nextDirection
                        break;
                    } else {
                        break;
                    }
                case "crossing":
                    if (cubeToCross !== null && cubeToCross[0] === getTensorPosition()[0] && cubeToCross[1] === getTensorPosition()[1]) {
                        if (distanceToCross === null) {
                            distanceToCross = CUBE_SIZE
                        } else if (distanceToCross > CUBE_SIZE / 2) {
                            distanceToCross -= moveMap(delta)
                            break;
                        } else if (distanceToCross > 0) {
                            if (carOrientation !== toDirection) {
                                setCarOrientation(toDirection)
                            }
                            distanceToCross -= moveMap(delta)
                            break;
                        } else {
                            distanceToCross = null
                            break;
                        }
                        break;
                    } else {
                        distanceToCross = null
                        state = "moving"
                        break;
                    }
            }
            addToPositionPath()
        }
    }

})
</script>
<template>
    <div class="container">
        <ResultModal :show-modal="showModal" @close-modal="resetMap()"/>
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

                    <TresMeshStandardMaterial v-if="cube.map === 'upDown'" :map="upDownTexture.map"/>
                    <TresMeshStandardMaterial v-else-if="cube.map === 'leftRight'" :map="leftRightTexture.map"/>
                    <TresMeshStandardMaterial v-else-if="cube.map === 'other'" :map="otherTexture.map"/>
                    <TresMeshStandardMaterial v-else-if="cube.map === 'grass'" :map="grassTexture.map"/>
                    <TresMeshStandardMaterial v-else :map="grassTexture.map"/>
                </TresMesh>
                <TresMesh v-for="(cube, index) in intersection" :key="index" :position="cube.position"
                          ref="intersectionRef">
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

let setShowModal = null
let getShowModal = null

let START = null
let END = null

let nextDirection = null

import tensor from '../data/tensor.json'
import speedTensor from '../data/speedTensor.json'
import stopTensor from '../data/stopTensor.json'
import { getMap } from '@/js/map.js'

export default {
    name: 'ThreeCanvas',
    components: {
        OrbitControls: OrbitControls,
        TresCanvas: TresCanvas,
    },
    data() {
        return {
            mapCenter: [15, 1, 13],
            car: {
                position: [15, 1, 13],
                color: 'orange',
                dimensions: [0.5, 0.5, 0.5]
            },
            map: [],
            showModal: false,
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
        resetMap() {
            setShowModal(false)
            this.tensorToMap()
            this.tensorToIntersection()
        },
        getShowModal() {
            return this.showModal
        },
        setShowModal(showModal) {
            this.showModal = showModal
        },
        robustGet(map, row, col = null) {
            if (row < 0) {
                return null
            }
            if (col < 0) {
                return null
            }
            if (map[row] === undefined) {
                return null
            }
            if (map[row][col] === undefined) {
                return null
            }
            return map[row][col]
        },
        findAppropriateMap(tensorCoordinate) {
            const row = tensorCoordinate[0];
            const col = tensorCoordinate[1];

            // if the cube at the right and the left are 1, and up and down are 0, then it's a left-right cube
            if (this.robustGet(this.tensor, row, col - 1) === 1 && this.robustGet(this.tensor, row, col + 1) === 1 && this.robustGet(this.tensor, row - 1, col) !== 1 && this.robustGet(this.tensor, row + 1, col) !== 1) {
                return 'upDown'
            }
            // if the cube at the right and the left are 0, and up and down are 1, then it's a up-down cube
            if (this.robustGet(this.tensor, row, col - 1) !== 1 && this.robustGet(this.tensor, row, col + 1) !== 1 && this.robustGet(this.tensor, row - 1, col) === 1 && this.robustGet(this.tensor, row + 1, col) === 1) {
                return 'leftRight'
            }
            return 'other'
        },
        move(direction) {
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
        findNextIntersection() {
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
            let startXOffset = this.start[0] * CUBE_SIZE
            let startZOffset = this.start[1] * CUBE_SIZE

            map.push({
                position: [this.end[0] * CUBE_SIZE - startXOffset, CAR_SIZE, this.end[1] * CUBE_SIZE - startZOffset],
                map: 'other',
                dimensions: [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE]
            })
            for (let i = 0; i < this.tensor.length; i++) {
                for (let j = 0; j < this.tensor[i].length; j++) {
                  if (this.tensor[i][j] === 1)
                  {
                    // Shows traffic
                    if (this.trafficTensor[i][j] < 0.25 ) map.push({position: [i, 0, j], color: 'black', dimensions: [1, 1, 1]})
                    else if (0.25 <= this.trafficTensor[i][j] && this.trafficTensor[i][j] < 0.5 ) map.push({position: [i, 0, j], color: 'yellow', dimensions: [1, 1, 1]})
                    else if (0.5 <= this.trafficTensor[i][j] && this.trafficTensor[i][j] < 0.75 ) map.push({position: [i, 0, j], color: 'orange', dimensions: [1, 1, 1]})
                    else if (0.75 <= this.trafficTensor[i][j]) map.push({position: [i, 0, j], color: 'red', dimensions: [1, 1, 1]})
                  }
                    if (this.tensor[i][j] === 0) map.push({position: [i, 0, j], color: '#41980A', dimensions: [1, 1, 1]})

                }
            }
            this.map = map
        },
        tensorToIntersection() {
            let startXOffset = this.start[0] * CUBE_SIZE
            let startZOffset = this.start[1] * CUBE_SIZE
            let intersection = []
            for (let i = 0; i < this.stopTensor.length; i++) {
                for (let j = 0; j < this.stopTensor[i].length; j++) {
                    if (this.stopTensor[i][j] === 1) intersection.push({
                        position: [i * CUBE_SIZE - startXOffset, CUBE_SIZE - CAR_SIZE, j * CUBE_SIZE - startZOffset],
                        color: 'red',
                        dimensions: [0.3 * CUBE_SIZE, 0.3 * CUBE_SIZE, 0.3 * CUBE_SIZE]
                    })
                    if (this.stopTensor[i][j] === 2) intersection.push({
                        position: [i * CUBE_SIZE - startXOffset, CUBE_SIZE - CAR_SIZE, j * CUBE_SIZE -startZOffset],
                        color: 'blue',
                        dimensions: [0.3 * CUBE_SIZE, 0.3 * CUBE_SIZE, 0.3 * CUBE_SIZE]
                    })
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
    async mounted() {
        START = this.start
        END = this.end
        setShowModal = this.setShowModal
        getShowModal = this.getShowModal
        this.tensorToIntersection();
        await this.fetchMap();
        this.tensorToMap();
    }

}
</script>

<style scoped>
img {
    filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(354deg) brightness(102%) contrast(101%);
}

.container {
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
    background-color: rgba(2, 0, 36, 0.3);
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
