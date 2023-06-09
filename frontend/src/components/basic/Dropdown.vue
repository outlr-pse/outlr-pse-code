<template>
  <div class="custom-dropdown">
    <button @click="openDropdown">
      <div class="buttonValue" :style="buttonStyle">
        {{ selectedOption }}
        <span class="material-icons md-dark" style="color: var(--color-stroke); font-size: 3vh;">{{ arrowDirection }}</span>
      </div>
    </button>
    <ul v-if="isOpen" class="custom-dropdown-options">
      <li v-for="option in options" @click="selectOption(option)" v-bind:key="option">{{ option }}</li>
    </ul>
  </div>

</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Dropdown',
  data () {
    return {
      isOpen: false,
      selectedOption: '',
      arrowDirection: 'chevron_right',
      buttonStyle: {
        color: 'var(--color-stroke)'
      }
    }
  },
  props: {
    hint: {
      type: String,
      required: false,
      default: 'Select an option'
    },
    options: {
      type: Array as () => string[],
      required: true
    },
    value: {
      type: String,
      required: false,
      default: null
    }
  },
  methods: {
    openDropdown () {
      this.isOpen = !this.isOpen
      this.arrowDirection = this.isOpen ? 'expand_more' : 'chevron_right'
    },
    selectOption (option: string) {
      this.selectedOption = option
      this.$emit('onValueSelected', option)
      this.isOpen = false
      this.arrowDirection = 'chevron_right'
    }
  },
  mounted () {
    if (this.value != null) {
      this.selectedOption = this.value
      this.buttonStyle = {
        color: 'var(--color-text)'
      }
    } else {
      this.selectedOption = this.hint
    }

    document.addEventListener('click', (event) => {
      if (!this.$el.contains(event.target)) {
        this.isOpen = false
        this.arrowDirection = 'chevron_right'
      }
    })
  },
  beforeUnmount () {
    document.removeEventListener('click', (event) => {
      if (!this.$el.contains(event.target)) {
        this.isOpen = false
        this.arrowDirection = 'chevron_right'
      }
    })
  },
  watch: {
    selectedOption: function (oldVal: string) {
      if (oldVal === this.hint) {
        this.buttonStyle = {
          color: 'var(--color-stroke)'
        }
      } else {
        this.buttonStyle = {
          color: 'var(--color-text)'
        }
      }
    }
  }
})
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
  width: 20vw;
  height: 5.5vh;
  padding-left: .6em;
  padding-right: .6em;
  border: none;
  background-color: transparent;
  text-align: start;
  font-size: 2.2vh;
  font-weight: 500;
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
  background-color: var(--color-selected);
  color: var(--color-background);
  cursor: default;
}
</style>
