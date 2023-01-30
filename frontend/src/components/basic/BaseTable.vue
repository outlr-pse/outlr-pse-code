<template>
    <table :style="style">
      <thead>
      <slot name="header"></slot>
      </thead>
      <tbody>
      <slot name="body"></slot>
      </tbody>
    </table>
</template>

<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({

  props: {
    style: {
      type: Object as () => CSSStyleDeclaration,
      required: false,
    },
  },
})
</script>

<style scoped>
</style>