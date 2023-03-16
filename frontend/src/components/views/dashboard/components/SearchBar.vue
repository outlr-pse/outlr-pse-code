<template>
  <div>
    <input
      v-model="searchTerm"
      type="text"
      :placeholder=" $t('message.dashboard.search')"
      class="field"
    >
    <ButtonComponent
      class="clear-button"
      :text=" $t('message.dashboard.clear')"
      :button-type="ButtonType.OUTLINE"
      :size="[100,47]"
      :text-size="[20,400]"
      @click="clear"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ButtonComponent from '../../../basic/button/ButtonComponent.vue'
import { ButtonType } from '../../../basic/button/ButtonType'

export default defineComponent({
  name: 'SearchBar',
  components: { ButtonComponent },
  data () {
    return {
      searchTerm: ''
    }
  },
  computed: {
    ButtonType () {
      return ButtonType
    }
  },
  watch: {
    searchTerm: function () {
      this.$emit('search-term-changed', this.searchTerm)
    }
  },
  methods: {
    clear () {
      this.searchTerm = ''
    }
  }
})
</script>

<style scoped>

.field {
  border: 1px solid var(--color-stroke);
  border-radius: 12px;
  padding: 1vh;
  font-size: 20px;
  font-weight: 600;
  background-color: var(--color-background);
}
.clear-button {
  margin-left: 1vw;
  margin-top: 1vh;
}

</style>
