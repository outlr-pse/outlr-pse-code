<template>
  <div style="height: 50vh">
    <div class="tableBox">
      <BaseTable :style="{ width: '100%'}">
        <template #header>
          <tr class="firstRow">
            <td v-for="header in headers" @click="headerClick(header)" class="headerCells">
              {{ header }}
            </td>
          </tr>
        </template>
        <template #body>
          <tr v-for="(row, rowIndex) in filteredData" @click="rowClick(row[0])" class="tableData">
            <td v-for="(cell, cellIndex) in row[1]" :key="cellIndex" @click="cellClick(row[0], rowIndex, cellIndex)">
              <div v-if="cellIndex === 0" class="cell">
                <Icon class="material-icons md-dark icon"
                      style="font-size: 2.5vh; font-weight: 100; color: var(--color-stroke)"
                      @click="iconClick(row[0], rowIndex)">chevron_right
                </Icon>
                {{ cell }}
              </div>
              <div v-else class="cell">
                 <div v-if="showDetails && rowIndex === selectedRow" class="details">
                  {{ cell }}
                </div>
                <div v-else>
                  {{ cell }}
                </div>
              </div>

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
import {DashboardSortColumn, getDashboardSortColumnLabel} from "./DashboardSortColumn";

export default defineComponent({
  components: {Card, BaseTable},
  data() {
    return {
      headers: [] as string[],
      data: [] as [number, string[]][],
      filteredData: [] as [number, string[]][],
      experiments: [] as Experiment[],
      experimentMap: new Map<number, Experiment>(),
      shownParams: [] as Hyperparameter[],
      showDetails: false,
      selectedRow: -1
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
      console.log("hello im watching currentSorting")
      this.tableSort(newSorting)
    }
  },
  methods: {
    headerClick(header: string) {
      let sortColumn = getDashboardSortColumnLabel(header)
      this.tableSort(sortColumn)
    },
    rowClick(row: number) {
      //this.$router.push("/experiment/" + row)
    },
    cellClick(id: number, rowIndex: number, cellIndex: number) {
      if (cellIndex == 0) {
        return
      } else {
        this.$router.push("/experiment/" + id)
      }
    },
    iconClick(id: number, rowIndex: number) {
      let experiment = this.experimentMap.get(id)
      if (experiment) {
        this.showDetails = !this.showDetails
        this.selectedRow = rowIndex
        this.shownParams = experiment.odm.hyperParameters
      }
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
  },
  async mounted() {
      this.experiments = await requestAllExperiments();
      this.headers = ["Name", "Dataset", "ODM", "Hyperparameter", "Date", "Accuracy"]

      for (let experiment of this.experiments) {
        this.experimentMap.set(experiment.id ? experiment.id : 0, experiment)
        if (experiment.running) {
          this.data.push([
            experiment.id ? experiment.id : 0,
            [
              experiment.name,
              experiment.datasetName,
              experiment.odm.name,
              "Running . . .",
              "",
              "",
            ]
          ])
        } else {
          let hyperParamString = ""
          for (let param of experiment.odm.hyperParameters) {
            hyperParamString += param.name + ": " + param.value + ", "
          }

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
  max-width: 7vw;

}

.cell {
  overflow: hidden;
  white-space: nowrap;
  display: flex;
  align-items: center;
}
.details{
  white-space: normal;
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

.headerCells {
  background-color: var(--color-cell-background);
  border: 1px solid var(--color-table-border);

}

td:hover.headerCells {
  background-color: var(--color-table-header);
  cursor: pointer;
}

.tableData td:hover {
  cursor: pointer;
}


</style>