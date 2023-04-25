<template>
    <TresCanvas clear-color="#82DBC5" window-size>
        <TresPerspectiveCamera />
        <OrbitControls/>
        <TresMesh>
            <TresBoxGeometry :args="[1, 1, 1]" />
            <TresMeshBasicMaterial color="orange" />
        </TresMesh>
        <TresMesh :position="[1, 0, 0]" >
            <TresBoxGeometry :args="[1, 1, 1]"/>
            <TresMeshBasicMaterial color="red"/>
        </TresMesh>
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
    }
}
</script>
