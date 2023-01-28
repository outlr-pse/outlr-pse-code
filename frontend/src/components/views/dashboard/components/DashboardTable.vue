<template>
  <BaseTable :style="style">
    <template #header>
      <tr>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Age</th>
      </tr>
    </template>
    <template #body>
      <tr>
        <td>John</td>
        <td>Doe</td>
        <td>43</td>
      </tr>
      <tr>
        <td>Mary</td>
        <td>Moe</td>
        <td>40</td>
      </tr>
      <tr>
        <td>July</td>
        <td>Dooley</td>
        <td>35</td>
      </tr>
    </template>
  </BaseTable>
</template>

<script lang="ts">
import BaseTable from "../../../basic/BaseTable.vue";
import {defineComponent} from "vue";

export default defineComponent({
  components: {BaseTable},
  props: {
    style: {
      type: Object as () => CSSStyleDeclaration,
      required: false,
    },
  },
})
</script>

<style scoped>

</style>