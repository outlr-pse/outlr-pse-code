<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <Tip text="This tip is useless."/>
    <DashboardTable
        :data="tableData"
        @rowClick="onRowClick"/>
  </div>
</template>

<script lang="ts">
import Tip from "../../basic/Tip.vue";
import {defineComponent} from "vue";
import {Experiment} from "../../../models/experiment/Experiment";
import {requestAllExperiments} from "../../../api/APIRequests";
import DashboardTable from "./components/DashboardTable.vue";

export default defineComponent({
  name: "Dashboard",
  components: {DashboardTable, Tip},
  data() {
    return {
      tableHeaders: [] as string[],
      tableData: [] as [number, string[]][],
      experiments: [] as Experiment[],

    }
  },
  methods: {
    applySearch(searchTerm: string) {

    },
    onRowClick(row: string[]){
      console.log(row)
    },
    onExperimentClick(experiment: Experiment) {
      this.$router.push({name: 'Experiment', params: {id: experiment.id}})
    }
  },
  async mounted() {
    this.experiments = await requestAllExperiments();
    this.tableHeaders = ["Name", "Dataset", "ODM", "Hyperparameter", "Date", "Accuracy"]

    for (let experiment of this.experiments) {
      if (experiment.running) {
        this.tableData.push([
          experiment.id ? experiment.id : 0,
          [
            experiment.name,
            experiment.datasetName,
            experiment.odm.name,
            "Running",
            "",
            "",
          ]
        ])
      } else {
        this.tableData.push([
          experiment.id ? experiment.id : 0,
          [
            experiment.name,
            experiment.datasetName,
            experiment.odm.name,
            experiment.odm.hyperParameters[0].name,
            experiment.experimentResult?.executionDate.toLocaleString() ?? "Not yet executed",
            experiment.experimentResult?.accuracy + "%",
          ]])
      }

    }

  }
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
  height: 100%;
  width: 100%;

}

</style>