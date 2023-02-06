<template>
  <Card>
    <div class="summary">
      Summary
    </div>
    <div style="border: 1px solid var(--color-stroke);"></div>
    <div style="height: 20vh; width: 25vw;padding-left: 2vw;padding-top: 2.5vh; padding-bottom: 2.5vh">
      <div class="row">
        <div class="textLeft">
          {{ $t('message.experimentResultView.experimentSummaryCard.odm') }}
        </div>
        <div>
          {{ experiment.odm.name }}
        </div>
      </div>
      <div class="row">
        <div class="textLeft">
          {{ $t('message.experimentResultView.experimentSummaryCard.accuracy') }}
        </div>
        <div>
          {{ experiment.experimentResult.accuracy }}
        </div>
      </div>
      <div class="row">
        <div class="textLeft">
          {{ $t('message.experimentResultView.experimentSummaryCard.executionDate') }}
        </div>
        <div>
          {{
            experiment.experimentResult.executionDate.getDay()
            + "." + (experiment.experimentResult.executionDate.getMonth() + 1)
            + "." + experiment.experimentResult.executionDate.getFullYear()
          }}
        </div>
      </div>
      <div class="row">
        <div class="textLeft">
          {{ $t('message.experimentResultView.experimentSummaryCard.executionTime') }}
        </div>
        <div>
          {{ experiment.experimentResult.executionTime }}
        </div>
      </div>
      <div class="row">
        <div class="textLeft">
          {{ $t('message.experimentResultView.experimentSummaryCard.detectedOutliers') }}
        </div>
        <div>
          {{ experiment.experimentResult.resultSpace.outliers.length }}
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
  props: {
    experiment: {
      type: Experiment,
      required: false,
      default: () => {
        return Experiment.fromJSON("{\"id\":3,\"name\":\"ExampleExperiment\",\"dataset_name\":\"ExampleDataset\",\"odm\":{\"name\":\"COPOD\",\"hyper_parameters\":[{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":true},{\"name\":\"n_jobs\",\"type\":\"integer\",\"optional\":true}]},\"param_values\":{\"contamination\":0.1,\"n_jobs\":-1},\"subspace_logic\":{\"operation\":{\"operator\":\"or\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1,\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1,\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}}]}}]}},\"experiment_result\":{\"accuracy\":null,\"execution_date\":\"2018-01-01T00:00:00.000Z\",\"execution_time\":29,\"result_space\":{\"id\":13,\"name\":\"Result\",\"columns\":[],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}}")
      },
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
  grid-template-columns: 75% 1fr;
  text-align: left;
  padding-top: 0.5vh;
  padding-bottom: 0.5vh;
}

.textLeft {
  color: var(--color-stroke);
}

</style>