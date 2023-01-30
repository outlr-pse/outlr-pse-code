<template>
  <ScollLayout :horizontal-scroll-bar="true" :vertical-scroll-bar="true">
    <table :style="style">
    <thead>
      <slot name="header"></slot>
    </thead>
    <tbody>
      <slot name="body"></slot>
    </tbody>
  </table>
  </ScollLayout>

</template>

<script lang="ts">
import {defineComponent} from "vue";
import ScollLayout from "./ScollLayout.vue";

export default defineComponent({
  components: {ScollLayout},
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