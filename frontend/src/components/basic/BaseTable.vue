<template>
  <table :style="style">
    <thead>
      <slot name="header" />
    </thead>
    <tbody>
      <slot name="body" />
    </tbody>
  </table>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({

  props: {
    style: {
      type: Object,
      required: false
    }
  }
})
</script>

<style scoped>
</style>
