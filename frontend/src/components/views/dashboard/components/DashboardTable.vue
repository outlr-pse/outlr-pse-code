<template>
  <div style="height: 50vh">
    <div class="tableBox">
      <BaseTable :style="{ width: '100%'}">
        <template #header>
          <tr class="firstRow">
            <td v-for="(header, index) in headers" @click="headerClick(header[1])" :class="headerClasses[index]">
              {{ header[0] }}
            </td>
          </tr>
        </template>
        <template #body>
          <tr v-for="row in filteredData" @click="rowClick(row[0])" class="tableData">
            <td v-for="cell in row[1]">
              {{ cell }}
            </td>
          </tr>
        </template>
      </BaseTable>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import BaseTable from "../../../basic/BaseTable.vue";
import {Experiment} from "../../../../models/experiment/Experiment";
import {requestAllExperiments} from "../../../../api/APIRequests";
import Card from "../../../basic/Card.vue";
import {Hyperparameter} from "../../../../models/odm/Hyperparameter";
import {DashboardSortColumn} from "./DashboardSortColumn";

export default defineComponent({
  components: {Card, BaseTable},
  data() {
    return {
      headers: [] as [string, DashboardSortColumn][],
      data: [] as [number, string[]][],
      filteredData: [] as [number, string[]][],
      experiments: [] as Experiment[],
      shownParams: [] as Hyperparameter[],
      headerClasses: ['col-1', 'col-2', 'col-3', 'col-4', 'col-5', 'col-6']
    }
  },
  props: {
    searchTerm: {
      type: String,
      required: true
    },
    currentSorting: {
      type: String,
      required: true
    }
  },

  watch: {
    searchTerm: function (newSearchTerm: string) {
      this.filteredData = this.data.filter((row) => {
        for (let cell of row[1]) {
          if (cell.toLowerCase().includes(newSearchTerm.toLowerCase())) {
            return true
          }
        }
        return false
      })
    },
    currentSorting: function (newSorting: DashboardSortColumn) {
      this.tableSort(newSorting)
    }
  },
  async mounted() {
    this.experiments = await requestAllExperiments();
    let headerShown = [
      this.$t('message.dashboard.name'),
      this.$t('message.dashboard.dataset'),
      this.$t('message.dashboard.odm'),
      this.$t('message.dashboard.hyperparameters'),
      this.$t('message.dashboard.date'),
      this.$t('message.dashboard.accuracy')
    ]
    this.headers = [
        [headerShown[0], DashboardSortColumn.NAME],
        [headerShown[1], DashboardSortColumn.DATASET],
        [headerShown[2], DashboardSortColumn.ODM],
        [headerShown[3], DashboardSortColumn.HYPERPARAMETER],
        [headerShown[4], DashboardSortColumn.DATE],
        [headerShown[5], DashboardSortColumn.ACCURACY]
    ]

    for (let experiment of this.experiments) {
      let hyperParamString = ""
      for (let param of experiment.odm.hyperParameters) {
        hyperParamString += param.name + ": " + param.value + ", "
      }
      if (experiment.running) {
        this.data.push([
          experiment.id ? experiment.id : 0,
          [
            experiment.name,
            experiment.datasetName,
            experiment.odm.name,
            hyperParamString,
            "Running . . .",
            "",
          ]
        ])
      } else {

        this.data.push([
          experiment.id ? experiment.id : 0,
          [
            experiment.name,
            experiment.datasetName,
            experiment.odm.name,
            hyperParamString,
            experiment.experimentResult?.executionDate.toLocaleString() ?? "Not yet executed",
            experiment.experimentResult?.accuracy + "%",
          ]])
      }
    }
    this.filteredData = this.data

  },
  methods: {
    headerClick(header: DashboardSortColumn) {
      this.tableSort(header)
    },
    rowClick(row: number) {
      this.$router.push("/experiment/" + row)
    },
    tableSort(sortColumn: DashboardSortColumn) {
      if (sortColumn === DashboardSortColumn.NAME) {
        this.filteredData.sort((a, b) => {
          return a[1][0].localeCompare(b[1][0])
        })
      } else if (sortColumn === DashboardSortColumn.DATASET) {
        this.filteredData.sort((a, b) => {
          return a[1][1].localeCompare(b[1][1])
        })
      } else if (sortColumn === DashboardSortColumn.ODM) {
        this.filteredData.sort((a, b) => {
          return a[1][2].localeCompare(b[1][2])
        })
      } else if (sortColumn === DashboardSortColumn.HYPERPARAMETER) {
        this.filteredData.sort((a, b) => {
          return a[1][3].localeCompare(b[1][3])
        })
      } else if (sortColumn === DashboardSortColumn.DATE) {
        this.filteredData.sort((a, b) => {
          return a[1][4].localeCompare(b[1][4])
        })
      } else if (sortColumn === DashboardSortColumn.ACCURACY) {
        this.filteredData.sort((a, b) => {
          return a[1][5].localeCompare(b[1][5])
        })
      }
    },

  }
})
</script>

<style scoped>

.tableBox {
  height: max-content;
  max-height: 50vh;
  width: 80vw;
  border-style: solid;
  border-radius: 7px;
  border-width: 2px;
  border-color: var(--color-table-border);
  overflow: auto;
}

table {
  width: 100%;
  height: 100%;
  position: sticky;
}

th {
  position: sticky;
  top: 0;
}

table, th, tr, td {
  border-collapse: collapse;
  border-bottom: 1px solid var(--color-table-border);
}

tr {
  text-align: left;
}

tr td {
  padding: 0.5em;
}

td {
  max-height: 1vh;
}

.firstRow {
  position: sticky;
  top: 0;
}


tr:nth-child(odd).tableData {
  background-color: var(--color-background);
}

tr:nth-child(even).tableData {
  background-color: var(--color-table-secondary);
}

.col-1, .col-2, .col-3, .col-4, .col-5, .col-6 {
  background-color: var(--color-cell-background);
  border: 1px solid var(--color-table-border);

}

td:hover.col-1, :hover.col-2, :hover.col-3, :hover.col-4, :hover.col-5, :hover.col-6 {
  background-color: var(--color-table-header);
  cursor: pointer;
}
.col-1{
  width: 15%;
}
.col-2{
  width: 15%;
}
.col-3{
  width: 10%;
}
.col-4{
  width: 42%;
}
.col-5{
  width: 15%;
}
.col-6{
  width: 3%;
}

.tableData td:hover {
  cursor: pointer;
}


</style>