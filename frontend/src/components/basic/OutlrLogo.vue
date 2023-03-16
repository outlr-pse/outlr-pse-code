<template>
  <img
    alt="Outlr logo"
    :style="{width: sizeStyle}"
    src="/src/assets/OutlrLogo.svg"
  >
</template>

<script lang="ts">
export default {
  name: 'OutlrLogo',
  props: {
    sizeStyle: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      path: '@/assets/OutlrLogo.svg'
    }
  }
}
</script>

<style scoped>

</style>
