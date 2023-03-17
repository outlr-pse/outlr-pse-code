<template>
  <div class="dropdown">
    <Dropdown :options="options" @onValueSelected="selectOption"/>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { DashboardSortColumn, getDashboardSortColumnLabel } from './DashboardSortColumn'
import Dropdown from '../../../basic/Dropdown.vue'

export default defineComponent({
  name: 'SortColumnSelector',
  components: { Dropdown },
  computed: {
    options () {
      return Object.values(DashboardSortColumn)
    }
  },
  methods: {
    selectOption (option: string) {
      this.$emit('onSortColumnSelected', getDashboardSortColumnLabel(option))
    }
  }
})
</script>

<style scoped>

</style>
