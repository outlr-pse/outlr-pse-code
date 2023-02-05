<template>
  <button :class="buttonType" :style="style" @click="onClick">
    <div v-if="IconProvided">
      <div style="display: inline-grid; grid-template-rows: auto auto; padding-top: 4vh">
        <div> {{ text }}</div>
        <div>
          <Icon class="material-icons md-dark icon" style="font-size: 4vh; font-weight: 100; color: var(--color-stroke)" > {{startIcon}} </Icon>
        </div>
    </div>
    </div>
    <div v-else>
      {{ text }}
    </div>
  </button>
</template>

<script lang="ts">
import {CSSProperties, defineComponent} from 'vue'
import { ButtonType } from './ButtonType'

export default defineComponent({
    props: {
      text:{
        type: String,
        required: false
      },
      buttonType:{
        type: String as () => ButtonType,
        default: ButtonType.DEFAULT,
        required: false
      },
      startIcon:{
        type: String,
        required: false
      },
      size:{
        type: Object as () => [number, number],
        required: false,
        default: [100, 50],
      },
      color:{
        type: String,
        required: false,
      },
      textSize:{
        type: Object as () => [number, CSSProperties['fontWeight']],
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
    style() : CSSProperties{
      return {
        width: this.size[0] + 'px',
        height: this.size[1] + 'px',
        backgroundColor: this.color,
        fontSize: this.textSize[0] != -1 ? this.textSize[0] + 'px' : '20px',
        fontWeight: this.textSize[1] != -1 ? this.textSize[1] : 500 ,
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

button:hover .icon{
  animation: wiggle 0.5s ease-in-out infinite alternate;
}

@keyframes wiggle {
  from {
    transform: translate(0, -2px);
  }
  to {
    transform: translate(0, 2px);
  }
}
</style>