<template>
    <TresCanvas clear-color="#82DBC5" window-size>
        <TresPerspectiveCamera />
        <OrbitControls/>
        <TresScene>
            <TresMesh v-for="(cube, index) in map" :key="index" :position="cube.position">
                <TresBoxGeometry :args="cube.dimensions"/>
                <TresMeshBasicMaterial :color="cube.color"/>
            </TresMesh>
        </TresScene>
        <TresAmbientLight :intensity="1"/>
    </TresCanvas>
</template>

<script>
import {extend, TresCanvas} from '@tresjs/core'
import { OrbitControls } from '@tresjs/cientos';
extend({ OrbitControls })
export default {
    name: 'ThreeCanvas',
    components:{
        TresCanvas: TresCanvas,
        OrbitControls: OrbitControls
    },
    data(){
        return{
          map:[
            {position: [0, 1, 2], color: 'orange', dimensions: [1, 1, 1]},

            {position: [0, 0, 0], color: 'grey', dimensions: [1, 1, 1]},
            {position: [1, 0, 0], color: 'grey', dimensions: [1, 1, 1]},
            {position: [2, 0, 0], color: 'grey', dimensions: [1, 1, 1]},
            {position: [3, 0, 0], color: 'grey', dimensions: [1, 1, 1]},
            {position: [4, 0, 0], color: 'grey', dimensions: [1, 1, 1]},

            {position: [0, 0, 1], color: 'black', dimensions: [1, 1, 1]},
            {position: [1, 0, 1], color: 'black', dimensions: [1, 1, 1]},
            {position: [2, 0, 1], color: 'black', dimensions: [1, 1, 1]},
            {position: [3, 0, 1], color: 'black', dimensions: [1, 1, 1]},
            {position: [4, 0, 1], color: 'black', dimensions: [1, 1, 1]},

            {position: [0, 0, 2], color: 'black', dimensions: [1, 1, 1]},
            {position: [1, 0, 2], color: 'yellow', dimensions: [1, 1, 1]},
            {position: [2, 0, 2], color: 'yellow', dimensions: [1, 1, 1]},
            {position: [3, 0, 2], color: 'black', dimensions: [1, 1, 1]},
            {position: [4, 0, 2], color: 'yellow', dimensions: [1, 1, 1]},

            {position: [0, 0, 3], color: 'black', dimensions: [1, 1, 1]},
            {position: [1, 0, 3], color: 'black', dimensions: [1, 1, 1]},
            {position: [2, 0, 3], color: 'black', dimensions: [1, 1, 1]},
            {position: [3, 0, 3], color: 'black', dimensions: [1, 1, 1]},
            {position: [4, 0, 3], color: 'black', dimensions: [1, 1, 1]},

            {position: [0, 0, 4], color: 'grey', dimensions: [1, 1, 1]},
            {position: [1, 0, 4], color: 'grey', dimensions: [1, 1, 1]},
            {position: [2, 0, 4], color: 'grey', dimensions: [1, 1, 1]},
            {position: [3, 0, 4], color: 'grey', dimensions: [1, 1, 1]},
            {position: [4, 0, 4], color: 'grey', dimensions: [1, 1, 1]},
          ]
        }
    }
}
</script>
