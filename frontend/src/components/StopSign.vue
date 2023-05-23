<script setup>
import {shallowRef} from "vue";
import {useFBX} from "@tresjs/cientos";

// eslint-disable-next-line no-undef,vue/valid-define-props
const props = defineProps(['position'])

const SIGN_SCALE = 0.002
let signRef = shallowRef()
let signInstance = await useFBX('/models/trafficLight.fbx')
signInstance.scale.set(SIGN_SCALE, SIGN_SCALE, SIGN_SCALE)
signInstance.position.set(props.position[0], 0, props.position[2])
signInstance.rotation.set(0, 0.75, 0)
signInstance.updateMatrixWorld()
</script>

<template>
    <Suspense>
        <TresMesh v-bind="signInstance" ref="signRef"/>
    </Suspense>
</template>