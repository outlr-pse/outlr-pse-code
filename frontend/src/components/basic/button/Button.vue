<template>
  <button :class="buttonType" @click="onClick">{{ text }} </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { ButtonType } from './ButtonType'

export default defineComponent({
    props: {
      text:{
        type: String,
        required: false
      },
      buttonType:{
        type: Object as () => ButtonType,
        default: 'default',
        required: false
      },
      startIcon:{
        type: ImageBitmapRenderingContext,
        required: false
      }
    },
  methods: {
    onClick(){
      if(this.buttonType === ButtonType.DISABLED) return;
      this.$emit('buttonClick')
      console.log(this.buttonType)
    }
  }
})
</script>

<style scoped>
@import "./button.css";
</style>