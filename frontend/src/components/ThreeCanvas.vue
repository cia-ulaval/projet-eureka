<template>
    <TresCanvas clear-color="#82DBC5" window-size>
        <TresPerspectiveCamera :position="[160, 90, 100]" />
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
import {OrbitControls} from '@tresjs/cientos';
import {createMap} from '@/assets/MapCreator';
extend({ OrbitControls })

export default {
    name: 'ThreeCanvas',
    components:{
        TresCanvas: TresCanvas,
        OrbitControls: OrbitControls
    },
    data(){
        return{
          map: []
        }
    },
    mounted() {
        const graphAsEdges = [[[0, 0], [15, 20]], [[15, 20], [30, 50]],[[50, 0], [15, 20]], [[30, 50], [15, 90]], [[30, 50], [160, 0]]];
        const gridSize = [160, 90];
        this.map = createMap(graphAsEdges, gridSize);
    }
}
</script>
