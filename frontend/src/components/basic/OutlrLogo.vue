<template>
  <img alt="Outlr logo" :style="{width: sizeStyle}" src="/src/assets/OutlrLogo.svg"/>
</template>

<style scoped>

</style>

<script lang="ts">
export default {
  name: "OutlrLogo",
  data() {
    return {
      path: "@/assets/OutlrLogo.svg"
    }
  },
  props: {
    sizeStyle: {
      type: Number,
      required: true
    }
  }
}
</script>