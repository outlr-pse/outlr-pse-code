<template>
  <input
    v-model="value"
    type="text"
    :placeholder="placeholder"
    class="field"
  >
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ParameterInputField',
  props: {
    placeholder: {
      type: String,
      required: true
    },
    parameterId: {
      type: Number,
      default: null
    },
    optional: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      value: ''
    }
  },
  watch: {
    value: function () {
      this.$emit('input-change', this.value, this.parameterId)
    }
  },
  mounted () {
    if (!this.optional) {
      this.optionalInput()
    }
  },
  methods: {
    wrongInput () {
      this.$el.style.border = '1px solid var(--color-close-button)'
    },
    correctInput () {
      this.$el.style.border = '1px solid var(--color-stroke)'
    },
    optionalInput () {
      this.$el.style.border = '1px solid var(--color-input-optional)'
    },
    checkData () {
      this.$emit('check-data')
    }
  }
})
</script>

<style scoped>
.field {
    border: 1px solid var(--color-stroke);
    width: 8.2vw;
    outline: none;
    background-color: transparent;
    font-size: 1em;
    padding: 0.5em;
    border-radius: 7px;
    margin: 5px;
    color: var(--color-main-white);
}

</style>
