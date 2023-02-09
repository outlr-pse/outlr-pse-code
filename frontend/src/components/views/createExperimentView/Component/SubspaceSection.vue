<template>
  <div class="header">
    {{ $t('message.experimentCreate.subspaceLogic') }}
    <span class="material-icons md-dark icon" @mouseenter="showTip = true" @mouseleave="showTip = false">
        info
    </span>
    <transition name="fade">
      <Card class="card" v-if="showTip" @mouseleave="showTip = false" @mouseenter="showTip = true">
        {{ $t('message.experimentCreate.logicHint') }}
      </Card>
    </transition>
    <div style="border: 1px solid var(--color-lines); margin-top: .5vh"/>
  </div>
  <div class="subspaceLogic">
    <textarea id="editing" class="inputField" placeholder="Enter Subspace Logic" v-model="value"/>
  </div>

</template>

<script lang="ts">
import {defineComponent} from "vue";
import Card from "../../../basic/Card.vue";

export default defineComponent({
  name: "SubspaceSection",
  components: {Card},
  data() {
    return {
      value: "",
      showTip: false
    }
  },
  watch: {
    value: function () {
      this.$emit("onInputChange", this.value)
    }
  },
  emits: ["onInputChange"]
})
</script>

<style scoped>

.header {
  position: relative;
  font-size: 1.2vw;
  text-align: left;
  padding: 5px;
  width: 12vw;
  height: 25%;
}

.subspaceLogic {
  height: 68%;
  display: flex;
  text-align: left;
  width: 100%;
}

.inputField {
  width: 100%;
  border-radius: 8px;
  outline: none;
  font-size: 2vh;
  padding: 10px;
  z-index: 1;
  background: transparent;
  font-family: Poppins, serif;
  resize: none;

}

.icon {
  color: var(--color-text);
  width: auto;
  font-size: 18px;
}

.icon:hover {
  cursor: pointer;
}

.card {
  position: absolute;
  top: 70%;
  left: 65%;
  right: 0;
  width: 10vw;
  height: max-content;
  background-color: rgb(47, 41, 58);
  z-index: 100;
  border-radius: 12px;
  border: 1px solid var(--color-stroke);
  font-size: 14px;
  padding: 10px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}


</style>