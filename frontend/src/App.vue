<template>
    <Suspense>
        <ThreeCanvas/>
    </Suspense>
</template>

<script>
import ThreeCanvas from "@/components/ThreeCanvas.vue";

export default {
  name: 'App',
  components: {
      ThreeCanvas: ThreeCanvas,
  }
}
</script>

