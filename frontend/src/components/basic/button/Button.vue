<template>
  <button :class="buttonType" :style="style" @click="onClick">{{ text }} </button>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { ButtonType } from './ButtonType'
import {Icon} from "../Icon";

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
        type: Object as () => Icon,
        required: false
      },
      size:{
        type: Object as () => [Number, Number],
        required: false,
        default: [100, 50],
      },
      color:{
        type: String,
        required: false,
      },
    },
  methods: {
    onClick(){
      if(this.buttonType === ButtonType.DISABLED) return;
      this.$emit('buttonClick')
    }
  },
  computed: {
    style(){
      return {
        width: this.size[0] + 'px',
        height: this.size[1] + 'px',
        backgroundColor: this.color,
      }
    }

  }
})
</script>

<style scoped>
@import "./button.css";


</style>