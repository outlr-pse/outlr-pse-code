<template>
  <Card v-if="show">
    <div class="tip">
      {{ text }}
      <span
        class="material-icons md-dark icon"
        @click="show = !show"
      > close </span>
    </div>
  </Card>
</template>

<script lang="ts">
import Card from './Card.vue'
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Tip',
  components: { Card },
  props: {
    text: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      show: true
    }
  }
})
</script>

<style scoped>
.icon:hover {
  cursor: pointer;
}

.icon {
  font-size: 4vh;
  color: var(--color-close-button);
  height: max-content;
  position: relative;
  top: 50%;
  -ms-transform: translateY(-50%);
  transform: translateY(-50%);

}

.tip {
  display: flex;
  justify-content: space-between;
  width: 90vw;
  text-align: left;
}

</style>
