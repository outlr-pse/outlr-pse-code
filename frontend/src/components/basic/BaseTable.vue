<template>
  <div class="base-table" :style="style">
    <table>
      <thead>
      <slot name="header"></slot>
      </thead>
      <tbody>
      <slot name="body"></slot>
      </tbody>
    </table>
  </div>
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
.base-table {
  overflow: auto;
}
</style>