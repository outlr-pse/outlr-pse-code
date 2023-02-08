<template>
  <div class="header">
    Subspace Logic
    <div style="border: 1px solid var(--color-lines); margin-top: .5vh"/>
  </div>
  <div class="subspaceLogic">
    <textarea id="editing" class="inputField" placeholder="Enter Subspace Logic" v-model="value"/>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  name: "SubspaceSection",
  data() {
    return {
      value: "",
    }
  },
  watch: {
    value: function () {
      this.$emit("input-change", this.value)
    }
  }
})
</script>

<style scoped>

.header {
  font-size: 1.2vw;
  text-align: left;
  padding: 5px;
  width: 12vw;
}

.subspaceLogic {
  display: flex;
  text-align: left;
  height: 77%;
  width: 100%;
}

.inputField {
  width: 100%;
  margin-top: 1vh;
  border-radius: 8px;
  outline: none;
  font-size: 20px;
  padding: 14px;
  z-index: 1;
  background: transparent;
  font-family: Poppins,serif ;

}

</style>