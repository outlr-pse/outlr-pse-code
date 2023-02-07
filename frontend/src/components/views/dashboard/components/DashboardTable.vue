<template>
  <div class="tableBox">
    <BaseTable :style="{ width: '100%'}">
      <template #header>
        <tr>
          <td v-for="header in headers" @click="headerClick(header)" class="firstRow">
            {{ header }}
          </td>
        </tr>
      </template>
      <template #body>
        <tr v-for="row in data" @click="rowClick(row[0])" class="tableData">
          <td v-for="cell in row[1]">
            {{ cell }}
          </td>
        </tr>
      </template>
    </BaseTable>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import BaseTable from "../../../basic/BaseTable.vue";
import {Experiment} from "../../../../models/experiment/Experiment";

export default defineComponent({
  components: {BaseTable},
  data() {
    return {
      headers: [] as string[],
      tableData: [] as [number, string[]][],
    }
  },
  props: {
    data: {
      type: Array as () => [number, string[]][],
      required: true,
    },
  },
  mounted() {
    this.headers = ["Name", "Dataset", "ODM", "Hyperparameter", "Date", "Accuracy"]
  },
  methods: {
    headerClick(header: string) {
      this.$emit('headerClick', header)
    },
    rowClick(row: number) {
      this.$emit('rowClick', row)
    }
  }
})
</script>

<style scoped>
.tableBox {
  height: max-content;
  max-height: 60vh;
  width: 90vw;
  border-style: solid;
  border-radius: 7px;
  border-width: 1px;
  border-color: var(--color-stroke);
  overflow: auto;
}

table {
  width: 100%;
  height: 100%;
  border-radius: 15px;
}

table, tr, td {
  border-collapse: collapse;
  border: 1px solid var(--color-stroke);
}

tr {
  text-align: left;
  height: 100%;
}

tr td {
  padding: 0.5em;
}

tr:nth-child(odd).tableData {
  background-color: var(--color-background);
}

tr:nth-child(even).tableData {
  background-color: var(--color-lines);
}

.firstRow {
  background-color: var(--color-cell-background);
  position: sticky;
  top: 0;
  border: 1px solid var(--color-stroke);

}

td:hover.firstRow {
  background-color: var(--palette-purple-7);
  cursor: pointer;
}

.tableData td:hover {
  cursor: pointer;
}


</style>