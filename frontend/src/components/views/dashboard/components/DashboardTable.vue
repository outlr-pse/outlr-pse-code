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
          <tr v-for="row in filteredData" @click="rowClick(row)" class="tableData">
            <td v-if="row[1][4][1] === 'Running . . .' " v-for="cell in row[1]" class="running">
              {{ cell[1] }}
            </td>
            <td v-else-if="row[1][4][1] === 'Failed :(' " v-for="cell in row[1]" class="failed">
              {{ cell[1] }}
            </td>
            <td v-for="cell in row[1]" v-else class="notRunning">
              {{ cell[1] }}
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
      data: [] as [number, [any, string][]][],
      filteredData: [] as [number, [any, string][]][],
      experiments: [] as Experiment[],
      shownParams: [] as Hyperparameter[],
      headerClasses: ['col-1', 'col-2', 'col-3', 'col-4', 'col-5', 'col-6'],
      intervalID: undefined as any,
      currentSearchTerm: '',
      currentSorting: DashboardSortColumn.DATE,
    }
  },
  props: {
    searchTerm: {
      type: String,
      required: true
    },
  },

  watch: {
    searchTerm: function (newSearchTerm: string) {
      this.currentSearchTerm = newSearchTerm
      this.tableSearch()
    },
  },
  async mounted() {

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

    await this.fetchExperiments()
    this.intervalID = setInterval(this.fetchExperiments, 3000);

  },
  beforeUnmount() {
    clearInterval(this.intervalID);
  },
  methods: {
    async fetchExperiments() {
      this.data = []
      this.experiments = []
      let response = await requestAllExperiments();
      if (response.error) {
        return
      }
      for (let experiment of response.data) {
        this.experiments.push(Experiment.fromJSON(experiment))
      }
      for (let experiment of this.experiments) {
        let hyperParamString = ""
        for (let param of experiment.odm.hyperParameters) {
          hyperParamString += param.name + ": " + param.value + ", "
        }
        if (experiment.failed) {
          this.data.push([
            experiment.id ? experiment.id : 0,
            [[experiment.name,experiment.name],
              [experiment.datasetName,experiment.datasetName],
              [experiment.odm.name,experiment.odm.name],
              [hyperParamString,hyperParamString],
              [0, "Failed :("],
              [0, ""],
            ]
          ])
        } else if (experiment.running) {
          this.data.push([
            experiment.id ? experiment.id : 0,
            [
              [experiment.name,experiment.name],
              [experiment.datasetName,experiment.datasetName],
              [experiment.odm.name,experiment.odm.name],
              [hyperParamString,hyperParamString],
              [ Number.POSITIVE_INFINITY, "Running . . ."],
              [0, experiment.id ? experiment.id.toString() : ""],
            ]
          ])
        } else {
          let nowDate = new Date()
          let experimentDate = experiment.experimentResult?.executionDate
          let dateString = ""
          let timeDiff = 0
          if(experimentDate) {
            timeDiff = nowDate.getTime() - experimentDate.getTime()
            if(timeDiff < 604800000 ) {
              let days = Math.floor(timeDiff / 86400000)
              let hours = Math.floor((timeDiff % 86400000) / 3600000)
              let minutes = Math.floor(((timeDiff % 86400000) % 3600000) / 60000)
              let seconds = Math.floor((((timeDiff % 86400000) % 3600000) % 60000) / 1000)
              if(days >  0) {
                dateString = days + "d ago"
              } else if (hours > 0) {
                dateString = hours + "h ago"
              } else if (minutes > 0) {
                dateString = minutes + "m ago"
              } else if (seconds > 0) {
                dateString = seconds + "s ago"
              } else {
                dateString = "Just now"
              }
            } else {
              dateString = experimentDate.toLocaleString()
            }
          }
          let accuracy = 0
          if(experiment.experimentResult){
            accuracy =  experiment.experimentResult?.accuracy*100
          }

          this.data.push([
            experiment.id ? experiment.id : 0,
            [
              [experiment.name,experiment.name],
              [experiment.datasetName,experiment.datasetName],
              [experiment.odm.name,experiment.odm.name],
              [hyperParamString,hyperParamString],
              [experimentDate?.getTime(), dateString],
              [accuracy, accuracy != null ? accuracy + "%" : "No GT"],
            ]
          ])
        }
      }
      this.filteredData = this.data
      this.tableSort()
      this.tableSearch()
    },
    headerClick(header: DashboardSortColumn) {
      this.currentSorting = header
      this.tableSort()
    },
    rowClick(row: [number, string[]]) {
      if (row[1][4] === "Running . . .") {
        return
      }
      this.$router.push("/experiment/" + row[0])
    },
    tableSearch() {
      this.filteredData = this.data.filter((row) => {
        for (let i = 0; i < row[1].length - 2; i++) {
          if (row[1][i][1].toLowerCase().includes(this.currentSearchTerm.toLowerCase())) {
            return true
          }
        }
        return false
      })
    },
    tableSort() {
      if (this.currentSorting === DashboardSortColumn.NAME) {
        this.filteredData.sort((a, b) => {
          return a[1][0][0].localeCompare(b[1][0][0])
        })
      } else if (this.currentSorting === DashboardSortColumn.DATASET) {
        this.filteredData.sort((a, b) => {
          return a[1][1][0].localeCompare(b[1][1][0])
        })
      } else if (this.currentSorting === DashboardSortColumn.ODM) {
        this.filteredData.sort((a, b) => {
          return a[1][2][0].localeCompare(b[1][2][0])
        })
      } else if (this.currentSorting === DashboardSortColumn.HYPERPARAMETER) {
        this.filteredData.sort((a, b) => {
          return a[1][3][0].localeCompare(b[1][3][0])
        })
      } else if (this.currentSorting === DashboardSortColumn.DATE) {
        this.filteredData.sort((a, b) => {
          return a[1][4][0] > b[1][4][0] ? -1 : 1
        })
      } else if (this.currentSorting === DashboardSortColumn.ACCURACY) {
        this.filteredData.sort((a, b) => {
          return a[1][5][0] > b[1][5][0] ? -1 : 1
        })
      }
    },
  },
})
</script>

<style scoped>

.tableBox {
  height: max-content;
  max-height: 65vh;
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

.col-1 {
  width: 15%;
}

.col-2 {
  width: 15%;
}

.col-3 {
  width: 10%;
}

.col-4 {
  width: 42%;
}

.col-5 {
  width: 15%;
}

.col-6 {
  width: 3%;
}

.running {
  color: var(--color-running);
}
.failed {
  color: var(--color-close-button);
}

.running:hover {
  cursor: default;
}

.notRunning:hover {
  cursor: pointer;
}


</style>