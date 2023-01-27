<template>
  <div class="dropdown">
    <label>{{ label }}</label>
    <select @change="selectionChange">
      <option value="" disabled selected hidden="">{{ hint }}</option>
      <option v-for="option in options">{{ option }}</option>
    </select>
  </div>


</template>

<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  props: {
    label: {
      type: String,
      required: true,
    },
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
      required: true,
      default: "",
    },
  },
  methods: {
    selectionChange(event: any) {
      this.$emit("onValueSelected", event.target.value);
    },
  },

  mounted() {
    console.log(this.hint)
  }
});
</script>

<style scoped>
.dropdown {
  display: inline-grid;
}
</style>