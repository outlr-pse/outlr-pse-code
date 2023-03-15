<template>
  <div >
    <input type="text" v-model="searchTerm" :placeholder=" $t('message.dashboard.search')" class="field" />
    <Button @click="clear" class="clear-button" :text=" $t('message.dashboard.clear')" :button-type="ButtonType.OUTLINE" :size="[100,47]" :text-size="[20,400]"></Button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Button from '../../../basic/button/Button.vue'
import { ButtonType } from '../../../basic/button/ButtonType'
import { Languages } from '../../../../language/Languages'

export default defineComponent({
  name: 'SearchBar',
  computed: {
    ButtonType () {
      return ButtonType
    }
  },
  components: { Button },
  data () {
    return {
      searchTerm: ''
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
