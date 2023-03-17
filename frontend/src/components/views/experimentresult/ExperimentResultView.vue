<template>
  <div v-if="experiment">
    <div v-if="experiment.failed" class="failed">
      <Card>
        <h1>Experiment failed</h1>
        <p style="color: var(--color-close-button)">Reason: {{ experiment.error }}</p>
      </Card>
    </div>
    <div v-else-if="!experiment.experimentResult.hasGtFile" class="summary">
        <ExperimentSummaryCard :experiment="experiment"/>
    </div>
    <div v-else class="summary">
      <div class="card">
        <ExperimentSummaryCard :experiment="experiment"/>
      </div>
      <div class="curve">
        <ROCCurve :experiment="experiment"/>
      </div>

    </div>
  </div>
</template>

<script lang="ts">
import ExperimentSummaryCard from './components/ExperimentSummaryCard.vue'
import { useRoute } from 'vue-router'
import { requestExperimentResult } from '../../../api/APIRequests'
import { Experiment } from '../../../models/experiment/Experiment'
import { defineComponent } from 'vue'
import Card from '../../basic/Card.vue'
import ROCCurve from './components/ROCCurve.vue'

export default defineComponent({
  name: 'ExperimentResultView',
  components: { ROCCurve, Card, ExperimentSummaryCard },
  data () {
    return {
      experiment: null as Experiment | null,
      dataReady: false
    }
  },
  async mounted () {
    const route = useRoute()
    const response = await requestExperimentResult(+route.params.expId)
    if (response.status === 200) {
      this.experiment = Experiment.fromJSON(response.data)
      this.dataReady = true
    }
  }
})
</script>

<style scoped>
.summary {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}

.card {
  padding-right: 3vw;
}

.curve {
  padding-left: 3vw;
}

.failed {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
}
</style>
