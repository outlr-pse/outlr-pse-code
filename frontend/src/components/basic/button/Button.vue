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