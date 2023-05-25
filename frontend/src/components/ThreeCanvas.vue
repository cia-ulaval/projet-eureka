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
const stopTexture = await useTexture({
    map: '/textures/stop.png'
});
const lightTexture = await useTexture({
    map: '/textures/light.png'
});

const CAR_SCALE = 0.001
const model = await useFBX('/models/Car.fbx')
model.scale.set(CAR_SCALE, CAR_SCALE, CAR_SCALE)
model.updateWorldMatrix(true, true)

const boxRef = shallowRef(null)
const intersectionRef = shallowRef(null)

const {onLoop} = useRenderLoop()

let carOrientation = "up"

function moveMap(delta) {
    const rowCol = getCarPosition()
    const row = rowCol[0]
    const col = rowCol[1]

    const speed = speedTensor[row][col] ** 2 / 1000

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

    model.position.x += dx * distance
    model.position.z += dy * distance
    model.updateWorldMatrix(true, true)
    return distance
}

function isNextCubeAnIntersection() {
    // according to the car position and orientation and the tensor, check if the next cube is an intersection, i.e one of the 3 values is 1
    // if it is, return true, else return false
    let rowCol = getCarPosition()
    let row = rowCol[0]
    let col = rowCol[1]

    switch (carOrientation) {
        case "up":
            if (row <= 0) {
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
            if (row <= 0) {
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
            if (col <= 0) {
                return tensor[row][col + 1] === 1;
            }
            return tensor[row][col + 1] === 1 || tensor[row][col - 1] === 1;
        case "right":
            if (col <= 0) {
                return tensor[row][col + 1] === 1;
            }
            return tensor[row][col + 1] === 1 || tensor[row][col - 1] === 1;
    }
}

function getAvailableTurns() {
    // according to the car position and orientation and the tensor, return the available turns
    // if there is no turn, return null
    let rowCol = getCarPosition()
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

let state = "moving"
let cubeToCross = null
let toDirection = null
let distanceToCross = null
let path = []
let isCarInstantiated = false
let isFirstTurnDone = false

function addToPositionPath() {
    let position = getCarPosition()
    if (path.length === 0) {
        path.push(position)
    } else {
        let last = path[path.length - 1]
        if (last[0] !== position[0] || last[1] !== position[1]) {
            path.push(position)
        }
    }
}

function isGreaterThan(n1, n2) {
    return (n1 - n2) > 0.0001
}

function isTheEndReached() {
    const rowCol = getCarPosition()
    const row = rowCol[0]
    const col = rowCol[1]

    return row === END[0] && col === END[1]
}

function instantiateCar() {
    model.position.set(START[0], 1/2, START[1])
    model.updateWorldMatrix(true, true)
    setCarOrientation("up")
}

function getCarPosition() {
    return [Math.round(model.position.x), Math.round(model.position.z)]
}

onLoop(({delta}) => {
    if(getShowModal()){
        return
    }
    if (model === null) {
        return
    }
    if (!isCarInstantiated) {
        if (START !== null) {
            instantiateCar()
            isCarInstantiated = true
        }
    }
    else{
        console.log("CubeSize="+ CUBE_SIZE + " state=" + state + " - carRealCoor="+ model.position.x +", "+model.position.z + " - cubeToCross" + cubeToCross + " - toDirection=" + toDirection + " - carOrientation=" + carOrientation + ' - distanceToCross='+distanceToCross + " - availableTurns=" + getAvailableTurns() + " - nextDirection=" + nextDirection + " - path=" + path + " - isTheEndReached=" + isTheEndReached())
        if (boxRef.value) {
            if (isTheEndReached() && getShowModal() === false) {
                isCarInstantiated = false
                setShowModal(true)
                return
            }
            if (!isFirstTurnDone) {
                if (nextDirection !== null && getAvailableTurns().includes(nextDirection)) {
                    state = "crossing"
                    toDirection = nextDirection
                    distanceToCross = CUBE_SIZE/2
                    isFirstTurnDone = true
                }
            }

            switch (state) {
                case "moving":
                    if (isNextCubeAnIntersection()) {
                        state = "stopped"
                        cubeToCross = getCarPosition()
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
                    if (cubeToCross !== null && cubeToCross[0] === getCarPosition()[0] && cubeToCross[1] === getCarPosition()[1]) {
                        if (distanceToCross === null) {
                            console.log("HERE 1")
                            distanceToCross = CUBE_SIZE
                        } else if (isGreaterThan(distanceToCross, CUBE_SIZE/2)) {
                            console.log("HERE 2 :" + distanceToCross + " > 0.5 = " + isGreaterThan(distanceToCross, CUBE_SIZE/2))
                            distanceToCross -= moveMap(delta)
                            break;
                        } else if (isGreaterThan(distanceToCross, 0)) {
                            console.log("HERE 3")
                            if (carOrientation !== toDirection) {
                                setCarOrientation(toDirection)
                            }
                            distanceToCross -= moveMap(delta)
                            break;
                        } else {
                            console.log("HERE 4")
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
            <TresPerspectiveCamera :position="[25, 15, 25]" :look-at="mapCenter"/>
            <OrbitControls/>
            <TresScene>
                <TresMesh v-for="(index) in mapSize[0]" :key="index" :position="[index - 1, 0.2, -1]">
                    <TresBoxGeometry :args="[1, 1.2, 1]"/>
                    <TresMeshBasicMaterial color="black"/>
                </TresMesh>
                <TresMesh v-for="(index) in mapSize[0]" :key="index" :position="[index - 1, 0.2, mapSize[1]]">
                    <TresBoxGeometry :args="[1, 1.2, 1]"/>
                    <TresMeshBasicMaterial color="black"/>
                </TresMesh>
                <TresMesh v-for="(index) in mapSize[1]" :key="index" :position="[-1 , 0.2, index - 1]">
                    <TresBoxGeometry :args="[1, 1.2, 1]"/>
                    <TresMeshBasicMaterial color="black"/>
                </TresMesh>
                <TresMesh v-for="(index) in mapSize[1]" :key="index" :position="[mapSize[0], 0.2, index - 1]">
                    <TresBoxGeometry :args="[1, 1.2, 1]"/>
                    <TresMeshBasicMaterial color="black"/>
                </TresMesh>
                <TresMesh v-for="(cube, index) in map" :key="index" :position="cube.position" ref="boxRef">
                    <TresBoxGeometry :args="cube.dimensions"/>
                    <TresMeshStandardMaterial v-if="cube.map === 'upDown'" :map="upDownTexture.map" :color="cube.color"/>
                    <TresMeshStandardMaterial v-else-if="cube.map === 'leftRight'" :map="leftRightTexture.map" :color="cube.color"/>
                    <TresMeshStandardMaterial v-else-if="cube.map === 'stop'" :map="stopTexture.map"/>
                    <TresMeshStandardMaterial v-else-if="cube.map === 'light'" :map="lightTexture.map"/>
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
            <TresAmbientLight :intensity="4"/>
            map.length/2
        </TresCanvas>
    </div>
</template>

<script>
import {TresCanvas} from '@tresjs/core'
import {OrbitControls} from "@tresjs/cientos";

const CUBE_SIZE = 1

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
            end : [],
            mapSize: [0, 0],
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

            if (this.intersection.stop.includes(`${row},${col}`)) {
                return 'stop'
            }
            if (this.intersection.light.includes(`${row},${col}`)) {
                return 'light'
            }

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

            map.push({
                position: [this.end[0] * CUBE_SIZE, 0, this.end[1] * CUBE_SIZE],
                map: 'other',
                dimensions: [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE]
            })
            for (let i = 0; i < this.tensor.length; i++) {
                for (let j = 0; j < this.tensor[i].length; j++) {
                    if (this.tensor[i][j] === 1)
                    {
                      let position = [i * CUBE_SIZE, 0, j * CUBE_SIZE]
                      let appropriateMap = this.findAppropriateMap([i, j])
                      let dimensions = [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE]
                      let color = 'white'
                      // Shows traffic
                      if (0.25 <= this.trafficTensor[i][j] && this.trafficTensor[i][j] < 0.5 ) color = 'yellow'
                      else if (0.5 <= this.trafficTensor[i][j] && this.trafficTensor[i][j] < 0.75 ) color = 'orange'
                      else if (0.75 <= this.trafficTensor[i][j]) color = 'red'
                      map.push({position: position, color: color, dimensions: dimensions, map: appropriateMap})
                    }
                    if (this.tensor[i][j] === 0) map.push({
                        position: [i * CUBE_SIZE, 0.02, j * CUBE_SIZE],
                        map: 'grass',
                        dimensions: [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE]
                    })
                }
            }
            this.map = map
        },
        tensorToIntersection() {
            let intersection = {"stop": [], "light": []}
            for (let i = 0; i < this.stopTensor.length; i++) {
                for (let j = 0; j < this.stopTensor[i].length; j++) {
                    if (this.stopTensor[i][j] === 1)
                        intersection.stop.push(`${i},${j}`)
                    if (this.stopTensor[i][j] === 2)
                        intersection.light.push(`${i},${j}`)
                }
            }
            this.intersection = intersection
        },
        async fetchMap() {
          const mapInfos = await getMap();
          this.start = mapInfos.start;
          this.end = mapInfos.end;
          this.trafficTensor = mapInfos.traffic;
          this.mapSize = [mapInfos.traffic.length, mapInfos.traffic[0].length];
      }
    },
    async mounted() {
        setShowModal = this.setShowModal
        getShowModal = this.getShowModal
        await this.fetchMap();
        START = this.start
        END = this.end
        this.tensorToIntersection();
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
