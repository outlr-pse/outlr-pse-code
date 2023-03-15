<template>
  <div class="tip">
      <slot></slot>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Card'
})
</script>

<style scoped>
.tip {
  background-color: transparent;
  border-color: var(--color-stroke);
  border-radius: 15px;
  border-style: solid;
  border-width: 1px;
  padding: 10px;
  width: max-content;
  height: max-content;
}
</style>
