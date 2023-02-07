<template>
  <Card>
    <div class="summary">
      {{ $t('message.experimentResultView.experimentSummaryCard.summary') }}
    </div>
    <div style="border: 1px solid var(--color-stroke);"></div>
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
          {{ experiment.experimentResult?.accuracy + "%" }}
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
import {defineComponent} from "vue";
import {Experiment} from "../../../../models/experiment/Experiment";
import Card from "../../../basic/Card.vue";
import {ODM} from "../../../../models/odm/ODM";
import {Subspace} from "../../../../models/results/Subspace";
import {Literal} from "../../../../models/subspacelogic/Literal";
import {Operation} from "../../../../models/subspacelogic/Operation";
import {Operator} from "../../../../models/subspacelogic/Operator";
import {Outlier} from "../../../../models/results/Outlier";
import {ExperimentResult} from "../../../../models/results/ExperimentResult";

export default defineComponent({
  name: "ExperimentSummaryCard",
  components: {Card},
  computed: {
    time() {
      let time = this.experiment.experimentResult?.executionTime;
      if (time == null) {
        return "0h 0m 0s 0ms 0µs";
      }
      let hours = Math.floor(time / 3600000000);
      let minutes = Math.floor((time % 3600000000) / 60000000);
      let seconds = Math.floor(((time % 3600000000) % 60000000) / 1000000);
      let milliseconds = Math.floor(((time % 3600000000) % 60000000) % 1000000 / 1000);
      let microseconds = Math.floor((((time % 3600000000) % 60000000) % 1000000) % 1000);
      return  (hours != 0? hours + "h " : "")
          + (minutes != 0? minutes + "m " : "")
          + (seconds != 0? seconds + "s " : "")
          + (milliseconds != 0? milliseconds + "ms " : "")
          + (microseconds != 0? microseconds + "µs" : "");
    },
    date() {
      return this.experiment.experimentResult?.executionDate.toLocaleString();
    }
  },
  props: {
    experiment: {
      type: Experiment,
      required: true,
    },
  },
})
</script>

<style scoped>

.summary {
  font-size: 3.5vh;
  font-weight: 500;
  text-align: left;
  padding: 2vh;
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
  height: 20vh;
  width: max-content;
  padding: 2.5vh 2vw;
}

</style>