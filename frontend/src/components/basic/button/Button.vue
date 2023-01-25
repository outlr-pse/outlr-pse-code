<template>
  <button :class="buttonType" :style="style" @click="onClick">
    <div v-if="IconProvided" style="padding: 20px ">
      <div style="display: inline-grid; grid-template-rows: auto auto; padding: 10px;">
        <div> {{ text }}</div>
        <div>
          <img :src="startIcon">
        </div>
    </div>
    </div>
    <div v-else>
      {{ text }}
    </div>

  </button>
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
        type: String as () => ButtonType,
        default: 'default',
        required: false
      },
      startIcon:{
        type: String as () => Icon,
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
      textSize:{
        type: Object as () => [Number, Number],
        required: false,
        default: [20, 500],
      }
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
        fontSize: this.textSize[0] != null ? this.textSize[0] + 'px' : '20px',
        fontWeight: this.textSize[1] != null ? this.textSize[1] : 500,
      }
    },
    IconProvided(){
      return this.startIcon != undefined;
    }
  }
})
</script>

<style scoped>
@import "./button.css";
</style>