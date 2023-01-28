<template>
  <div class="custom-dropdown">
    <button @click="openDropdown">
      <div class="buttonValue">
        {{ selectedOption }} <img :src="arrowDirection">
      </div>
    </button>
    <ul v-if="isOpen" class="custom-dropdown-options">
      <li v-for="option in options" @click="selectOption(option)">{{ option }}</li>
    </ul>
  </div>

</template>

<script lang="ts">
import {defineComponent} from "vue";
import {Icon} from "./Icon";

export default defineComponent({
  computed: {
    Icon() {
      return Icon
    }
  },
  data() {
    return {
      isOpen: false,
      selectedOption: this.value != null ? this.value : this.hint,
      arrowDirection: Icon.EXPAND_RIGHT
    }
  },
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
      default: null,
    },
  },
  methods: {
    openDropdown() {
      this.isOpen = !this.isOpen;
      this.arrowDirection = this.isOpen ? Icon.EXPAND_DOWN : Icon.EXPAND_RIGHT;
    },
    selectOption(option: string) {
      this.selectedOption = option;
      this.$emit("onValueSelected", option);
      this.isOpen = false;
      this.arrowDirection = Icon.EXPAND_RIGHT;
    }
  },
  //TODO: CHATGPT sagt dass das ein memory leak erzeugen könnte muss man vielleicht beobachten
  mounted() {
    document.addEventListener("click", (event) => {
      if (!this.$el.contains(event.target)) {
        this.isOpen = false;
        this.arrowDirection = Icon.EXPAND_RIGHT;
      }
    });
  },
  beforeDestroy() {
    document.removeEventListener("click", (event) => {
      if (!this.$el.contains(event.target)) {
        this.isOpen = false;
        this.arrowDirection = Icon.EXPAND_RIGHT;
      }
    });
  }
});
</script>

<style scoped>

.custom-dropdown {
  position: relative;
  border-radius: 8px;
  border: thin solid var(--color-stroke);
  width: max-content;
  background-color: var(--color-background);
}

.custom-dropdown button {
  width: 30vw;
  height: 7vh;
  padding: 10px;
  border: none;
  background-color: transparent;
  text-align: start;
  font-size: 2.5vh;
}

.buttonValue {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.custom-dropdown-options {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 1;
  list-style: none;
  padding: 0;
  margin: 0;
  border-radius: 8px;
  border: thin solid var(--color-stroke);
  background-color: var(--color-background);
  overflow: auto;
  max-height: 45vh;
}

.custom-dropdown-options li {
  padding: 6px;
  text-align: start;
}

.custom-dropdown-options li:hover {
  background-color: var(--color-stroke);
  cursor: default;
}
</style>