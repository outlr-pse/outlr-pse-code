<template>
  <div style="height: 50vh">
    <div class="tableBox">
      <BaseTable :style="{ width: '100%'}">
        <template #header>
          <tr class="firstRow">
            <td v-for="(header, index) in headers" @click="headerClick(header[1])" :class="headerClasses[index]" v-bind:key="index">
              {{ header[0] }}
            </td>
          </tr>
        </template>
        <template #body>
          <tr v-for="row in filteredData" class="tableData" v-bind:key="row[0]" @click="rowClick(row)">
            <td v-for="cell in row[1]" v-bind:key="cell[1]"
                v-bind:class="[{'running': row[1][3][0] === -2},
                {'failed': row[1][3][0] === -1},
                {'notRunning': row[1][3][0] !== -2 && row[1][4][0] !== -1 }]">
              <div>
                {{ cell[1] }}
              </div>
            </td>
          </tr>
        </template>
      </BaseTable>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import BaseTable from '../../../basic/BaseTable.vue'
import { Experiment } from '../../../../models/experiment/Experiment'
import { requestAllExperiments } from '../../../../api/APIRequests'
import { Hyperparameter } from '../../../../models/odm/Hyperparameter'
import { DashboardSortColumn } from './DashboardSortColumn'
import { dateCalculation } from './DashboardUtil'

export default defineComponent({
  components: { BaseTable },
  data () {
    return {
      headers: [] as [string, DashboardSortColumn][],
      data: [] as [number, [any, string][]][],
      filteredData: [] as [number, [any, string][]][],
      experiments: [] as Experiment[],
      shownParams: [] as Hyperparameter[],
      headerClasses: ['col-1', 'col-2', 'col-3', 'col-4', 'col-5', 'col-6'],
      intervalID: undefined as any,
      currentSearchTerm: '',
      currentSorting: DashboardSortColumn.DATE
    }
  },
  props: {
    searchTerm: {
      type: String,
      required: true
    }
  },

  watch: {
    searchTerm: function (newSearchTerm: string) {
      this.currentSearchTerm = newSearchTerm
      this.tableSearch()
    }
  },
  async mounted () {
    const headerShown = [
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
    this.intervalID = setInterval(this.fetchExperiments, 3000)
  },
  beforeUnmount () {
    clearInterval(this.intervalID)
  },
  methods: {
    async fetchExperiments () {
      this.data = []
      this.experiments = []
      const response = await requestAllExperiments()
      if (response.error) {
        return
      }
      for (const experiment of response.data) {
        this.experiments.push(Experiment.fromJSON(experiment))
      }
      for (const experiment of this.experiments) {
        const id = experiment.id
        type TableCell = [any, string]; // [metaData for sorting, string representation]
        type TableRow = [number, TableCell[]]; // [id, [TableCell]]
        const row: TableRow = [id, []]

        for (const header of this.headers) { // 6 headers
          let cell: TableCell = [undefined, '']
          const shownParams = experiment.odm.hyperParameters
          const shownParamString = shownParams.map((param: { name: string; value: string; }) => {
            return param.name + ': ' + param.value
          }).join(', ')

          switch (header[1]) {
            case DashboardSortColumn.NAME:
              cell = [experiment.name, experiment.name]
              break
            case DashboardSortColumn.DATASET:
              cell = [experiment.datasetName, experiment.datasetName]
              break
            case DashboardSortColumn.ODM:
              cell = [experiment.odm.name, experiment.odm.name]
              break
            case DashboardSortColumn.HYPERPARAMETER:
              if (experiment.failed) {
                cell = [-1, 'Failed :(']
              } else if (experiment.running) {
                cell = [-2, 'Running ...']
              } else {
                cell = [shownParams, shownParamString]
              }
              break
            case DashboardSortColumn.DATE:
              cell = [experiment.creationDate,
                dateCalculation(experiment.creationDate ? experiment.creationDate : new Date())]
              break
            case DashboardSortColumn.ACCURACY:
              if (experiment.running || experiment.failed) {
                cell = [undefined, '']
              } else {
                const accuracy = experiment.experimentResult?.accuracy ? experiment.experimentResult?.accuracy * 100 : -1
                cell = [accuracy, accuracy !== -1 ? accuracy.toFixed(1) + '%' : 'No GT']
              }
              break
          }
          row[1].push(cell)
        }
        this.data.push(row)
      }
      this.filteredData = this.data
      this.tableSort()
      this.tableSearch()
    },
    headerClick (header: DashboardSortColumn) {
      this.currentSorting = header
      this.tableSort()
    },
    rowClick (row: [number, [any, string][]]) {
      if (row[1][4][0] === Infinity) {
        return
      }
      this.$router.push('/experiment/' + row[0])
    },
    tableSearch () {
      this.filteredData = this.data.filter((row) => {
        for (let i = 0; i < row[1].length - 2; i++) {
          if (row[1][i][1].toLowerCase().includes(this.currentSearchTerm.toLowerCase())) {
            return true
          }
        }
        return false
      })
    },
    tableSort () {
      const sortedData = this.data

      if (this.currentSorting === DashboardSortColumn.NAME) {
        sortedData.sort((a, b) => {
          return a[1][0][0].localeCompare(b[1][0][0])
        })
      } else if (this.currentSorting === DashboardSortColumn.DATASET) {
        sortedData.sort((a, b) => {
          return a[1][1][0].localeCompare(b[1][1][0])
        })
      } else if (this.currentSorting === DashboardSortColumn.ODM) {
        sortedData.sort((a, b) => {
          return a[1][2][0].localeCompare(b[1][2][0])
        })
      } else if (this.currentSorting === DashboardSortColumn.HYPERPARAMETER) {
        sortedData.sort((a, b) => {
          return a[1][3][0].localeCompare(b[1][3][0])
        })
      } else if (this.currentSorting === DashboardSortColumn.DATE) {
        sortedData.sort((a, b) => {
          return a[1][4][0] > b[1][4][0] ? -1 : 1
        })
      } else if (this.currentSorting === DashboardSortColumn.ACCURACY) {
        sortedData.sort((a, b) => {
          return a[1][5][0] > b[1][5][0] ? -1 : 1
        })
      }
      this.filteredData = sortedData
    }
  }
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
   padding: 0.5rem;
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
.notRunning {
  color: var(--color-text);
}

.running:hover {
  cursor: default;
}

.notRunning:hover {
  cursor: pointer;
}
.failed:hover {
  cursor: pointer;
}
</style>
