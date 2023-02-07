<template>
  <div class="dashboard">
    <h1>Dashboard</h1>

    <Tip text="This tip is useless."/>
    <div v-for="experiment in experiments" :key="experiment.id">
      {{ experiment.name }}

    </div>
  </div>
</template>

<script lang="ts">
import Tip from "../../basic/Tip.vue";
import {defineComponent} from "vue";
import {Experiment} from "../../../models/experiment/Experiment";
import {requestAllExperiments} from "../../../api/APIRequests";

export default defineComponent({
  name: "Dashboard",
  components: {Tip},
  data() {
    return {
      tableHeaders: [],
      tableData: [],
      filteredTableData: [],
      experiments: [Experiment]
    }
  },
  methods: {
    applySearch(searchTerm: string) {

    },
    onExperimentClick(experiment: Experiment) {
      this.$router.push({name: 'Experiment', params: {id: experiment.id}})
    }
  },
  async mounted() {
    this.experiments = await requestAllExperiments();
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