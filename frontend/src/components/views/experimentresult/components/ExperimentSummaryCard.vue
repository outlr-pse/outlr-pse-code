<template>
  <Card>
    <div class="summary">
      <h4 class="header">
        {{ experiment.name }}
      </h4>
      <ButtonComponent
        text="Download"
        :button-type="ButtonType.CONTRAST"
        :size="[120,40]"
        @buttonClick="download"
      />
    </div>
    <div style="border: 1px solid var(--color-stroke);" />
    <div class="content">
      <div class="row">
        <div class="textLeft">
          {{ $t('message.experimentResultView.experimentSummaryCard.odm') + ":" }}
        </div>
        <div>
          {{ experiment.odm.name }}
        </div>
      </div>
      <div class="row">
        <div class="textLeft">
          {{ $t('message.experimentResultView.experimentSummaryCard.accuracy') + ":" }}
        </div>
        <div>
          {{ experiment.experimentResult?.accuracy != null ? experiment.experimentResult?.accuracy*100 + "%" : "No GT" }}
        </div>
      </div>
      <div class="row">
        <div class="textLeft">
          {{ $t('message.experimentResultView.experimentSummaryCard.auc') + ":" }}
        </div>
        <div>
          {{ experiment.experimentResult?.hasGtFile ? experiment.experimentResult?.auc : "No GT" }}
        </div>
      </div>
      <div class="row">
        <div class="textLeft">
          {{ $t('message.experimentResultView.experimentSummaryCard.executionDate') + ":" }}
        </div>
        <div>
          {{ date }}
        </div>
      </div>
      <div class="row">
        <div class="textLeft">
          {{ $t('message.experimentResultView.experimentSummaryCard.executionTime') + ":" }}
        </div>
        <div>
          {{ time }}
        </div>
      </div>
      <div class="row">
        <div class="textLeft">
          {{ $t('message.experimentResultView.experimentSummaryCard.detectedOutliers') + ":" }}
        </div>
        <div>
          {{ experiment.experimentResult?.resultSpace?.outliers?.length }}
        </div>
      </div>
    </div>
  </Card>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { Experiment } from '../../../../models/experiment/Experiment'
import Card from '../../../basic/Card.vue'
import ButtonComponent from '../../../basic/button/ButtonComponent.vue'
import { ButtonType } from '../../../basic/button/ButtonType'
import { downloadExperiment } from '../../../../api/APIRequests'

export default defineComponent({
  name: 'ExperimentSummaryCard',
  components: { ButtonComponent, Card },
  props: {
    experiment: {
      type: Experiment,
      required: true
    }
  },
  computed: {
    ButtonType () {
      return ButtonType
    },
    time () {
      const time = this.experiment.experimentResult?.executionTime
      if (time == null) {
        return '0h 0m 0s 0ms 0µs'
      }
      const hours = Math.floor(time / 3600000000)
      const minutes = Math.floor((time % 3600000000) / 60000000)
      const seconds = Math.floor(((time % 3600000000) % 60000000) / 1000000)
      const milliseconds = Math.floor(((time % 3600000000) % 60000000) % 1000000 / 1000)
      const microseconds = Math.floor((((time % 3600000000) % 60000000) % 1000000) % 1000)
      return (hours !== 0 ? hours + 'h ' : '') +
          (minutes !== 0 ? minutes + 'm ' : '') +
          (seconds !== 0 ? seconds + 's ' : '') +
          (milliseconds !== 0 ? milliseconds + 'ms ' : '') +
          (microseconds !== 0 ? microseconds + 'µs' : '')
    },
    date () {
      return this.experiment.experimentResult?.executionDate.toLocaleString()
    }
  },
  methods: {
    download () {
      if (this.experiment.id == null) {
        return
      }
      downloadExperiment(this.experiment)
    }
  }
})
</script>

<style scoped>

.summary {
  font-size: 3.5vh;
  font-weight: 500;
  text-align: left;
  padding-left: 1vh;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.row {
  display: grid;
  grid-template-columns: 37vh 1fr;
  text-align: left;
  padding-top: 0.5vh;
  padding-bottom: 0.5vh;
}

.textLeft {
  color: var(--color-stroke);
}

.content {
  height: max-content;
  width: max-content;
  padding: 2.5vh 2vw 1vh;
}

.header {
  margin: 15px;
  width: 50%;
}

</style>
