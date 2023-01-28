<template>
  <div class="scroll-layout">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  props:{
    verticalScrollBar:{
      type: Boolean,
      default: false,
      required: false
    },
    horizontalScrollBar:{
      type: Boolean,
      default: false,
      required: false
    }
  }

})
</script>

<style scoped>
.scroll-layout{
  overflow: hidden;
  height: 100%;
  width: 100%;
}
.scroll-layout::-webkit-scrollbar {
  width: 0px;
  background: transparent;
}
.scroll-layout:hover{
  overflow: auto;
}


</style>