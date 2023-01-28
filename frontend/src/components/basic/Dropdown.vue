<template>
  <div class="dropdown">
    <!--  <label v-if="label != null" style="text-align: start; padding-left: 5px; padding-right: 5px;">{{ label }}</label> -->
    <select :value="value" @change="selectionChange" class="selectItem">
        <option value="" disabled selected hidden="">{{ hint }}</option>
        <option v-for="option in options">{{ option }}</option>
    </select>
  </div>


</template>

<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  props: {
    hint: {
      type: String,
      required: false,
      default: "Select an option",
    },
    options: {
      type: Array,
      required: true,
    },
    value: {
      type: String,
      required: false,
      default: "",
    },
  },
  methods: {
    selectionChange(event: any) {
      this.$emit("onValueSelected", event.target.value);
    },
  },
});
</script>

<style scoped>
.dropdown {
  display: inline-grid;
  height: auto;
  width: auto;
}

.selectItem {
  width: 300px;
  height: 50px;
  border-radius: 8px;
  background: var(--color-background);
  font-size: 2.6vh;
  padding-left: 1vh;
  text-overline-color: var(--color-main);
}
option{
  line-height: 10vh;
}

</style>