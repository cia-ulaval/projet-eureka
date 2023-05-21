<script setup>
import {useFBX} from '@tresjs/cientos'
import {shallowRef} from "vue";
import {useRenderLoop, useTexture} from "@tresjs/core";


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

let carPosition = [0, 0]
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

function getTensorPosition() {
    let row = Math.round(carPosition[0] / CUBE_SIZE);
    let col = Math.round(carPosition[1] / CUBE_SIZE);
    return [row, col]
}

let state = "moving"
let cubeToCross = null
let toDirection = null
let distanceToCross = null
let path = []

// TODO : Ajouter tous les points en coordonnée tenseur aux path (ne pas dupliquer précedent)
// TODO: change base car position
// TODO: caller un truc lorsque la voiture est sur la fin

onLoop(({delta}) => {
    console.log("state=" + state + " - toDirection=" + toDirection + " - carOrientation=" + carOrientation)
    if (boxRef.value) {
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
                    console.log("availableTurns=" + getAvailableTurns())
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
                            carOrientation = toDirection
                            path.push(toDirection)
                        }
                        distanceToCross -= moveMap(delta)
                        break;
                    } else {
                        // state = "moving"
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
    data() {
        return {
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
            for (let i = 0; i < this.tensor.length; i++) {
                for (let j = 0; j < this.tensor[i].length; j++) {
                    if (this.tensor[i][j] === 1) map.push({
                        position: [i * CUBE_SIZE, -CAR_SIZE, j * CUBE_SIZE],
                        map: this.findAppropriateMap([i, j]),
                        dimensions: [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE]
                    })
                    if (this.tensor[i][j] === 0) map.push({
                        position: [i * CUBE_SIZE, -CAR_SIZE, j * CUBE_SIZE],
                        map: 'grass',
                        dimensions: [CUBE_SIZE, CUBE_SIZE, CUBE_SIZE]
                    })
                }
            }
            this.map = map
        },
        tensorToIntersection() {
            let intersection = []
            for (let i = 0; i < this.stopTensor.length; i++) {
                for (let j = 0; j < this.stopTensor[i].length; j++) {
                    if (this.stopTensor[i][j] === 1) intersection.push({
                        position: [i * CUBE_SIZE, CUBE_SIZE - CAR_SIZE, j * CUBE_SIZE],
                        color: 'red',
                        dimensions: [0.3 * CUBE_SIZE, 0.3 * CUBE_SIZE, 0.3 * CUBE_SIZE]
                    })
                    if (this.stopTensor[i][j] === 2) intersection.push({
                        position: [i * CUBE_SIZE, CUBE_SIZE - CAR_SIZE, j * CUBE_SIZE],
                        color: 'blue',
                        dimensions: [0.3 * CUBE_SIZE, 0.3 * CUBE_SIZE, 0.3 * CUBE_SIZE]
                    })
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
