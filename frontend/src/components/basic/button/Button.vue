<template>
  <button :class="buttonType" :style="style" @click="onClick">
    <div v-if="IconProvided">
      <div style="display: inline-grid; grid-template-rows: auto auto;">
        <div> {{ text }}</div>
        <div>
          <span class="material-icons md-dark icon" style="font-size: 30px; font-weight: 100; color: var(--color-stroke)" > {{startIcon}} </span>
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
        type: String,
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
        default: [16, 500],
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

.icon {
    position: absolute;
    transform: translate(-16px, -10px);
}

button:hover .icon{
  position: absolute;
  transform: translate(-16px, -10px);
  animation: wiggle 0.5s ease-in-out infinite alternate;
}

@keyframes wiggle {
  from {
    transform: translate(-16px, -8px);
  }
  to {
    transform: translate(-16px, -12px);
  }
}
</style>