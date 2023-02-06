<script setup lang="ts">
import { ref } from 'vue'
import {Languages} from "../../language/Languages";
import Button from "../basic/button/Button.vue";
import {ButtonType} from "../basic/button/ButtonType";
import Tip from "../basic/Tip.vue";
import ExperimentSummaryCard from "./experimentresult/components/ExperimentSummaryCard.vue";
import {Experiment} from "../../models/experiment/Experiment";

defineProps<{ msg: string }>()

const count = ref(0)
</script>


<template>


  <ExperimentSummaryCard :experiment='Experiment.fromJSON("{\"id\":3,\"name\":\"ExampleExperiment\",\"dataset_name\":" +
            "\"ExampleDataset\",\"odm\":{\"name\":\"DEFAULT\",\"hyper_parameters\":[{\"name\":\"contamination\"," +
            "\"type\":\"numeric\",\"optional\":true},{\"name\":\"n_jobs\",\"type\":\"integer\",\"optional\":true}]}," +
            "\"param_values\":{\"contamination\":0.1,\"n_jobs\":-1},\"subspace_logic\":{\"operation\":{\"operator\":" +
            "\"or\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1," +
            "\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace" +
            "\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{" +
            "\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns" +
            "\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name" +
            "\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":" +
            "\"and\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1," +
            "\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace" +
            "\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{" +
            "\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns" +
            "\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name" +
            "\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}}]}}]}},\"experiment_result\":{" +
            "\"accuracy\":100,\"execution_date\":\"1000-01-01T00:00:00.000Z\",\"execution_time\":99999,\"result_space" +
            "\":{\"id\":13,\"name\":\"Result\",\"columns\":[],\"outliers\":[],\"roc_curve\":null}}}")'/>

  <Tip text="Hello Simon mach einfach irgendwas einfach irgendwas genau irgenwdas an text schreibst du jetzt da hin und noch bisschen mehr als nur irgendwas"></Tip>

  <Button text="Run experiment" :button-type="ButtonType.ACTIVE" :size="[421, 78]" :text-size="[30, 900]"/>
  <Button text="Create experiment" :button-type="ButtonType.ACTIVE" :size="[188, 45]" :text-size="[-1, -1]"/>
  <Button text="Sign Up" :button-type="ButtonType.DEFAULT" :size="[200, 100]" color="var(--color-purple-button)"/>
  <Button text="Navigate to dashboard" :button-type="ButtonType.DEFAULT" :size="[543, 100]" :text-size="[25, 400]" color="var(--color-purple-button)" start-icon="expand_more"/>
  <Button text="Refresh" :button-type="ButtonType.OUTLINE" :size="[127, 45]" />
  <Button text="Clear" :button-type="ButtonType.OUTLINE" :size="[127, 45]" />
  <Button text="Try it out" :button-type="ButtonType.OUTLINE" :size="[200, 100]" />
  <Button text="Sign Up" :button-type="ButtonType.OUTLINE" :size="[104, 52]" />
  <Button text="Login" :button-type="ButtonType.TRANSPARENT" :size="[104, 52]" />
  <Button text="DownloadCSV" :button-type="ButtonType.CONTRAST" :size="[217, 45]" />
  <Button text="Run experiment" :button-type="ButtonType.DISABLED" :size="[421, 78]"/>



  <Button text="Click me" @buttonClick="count++" :button-type="ButtonType.DEFAULT" :size="[100, 50]" color="var(--color-purple-button)" />

  <h1>{{ $t('message.greeting') }}, {{$t('message.name')}}</h1>

  <div class="tip">
    <Button @buttonClick="count % 2 === 0 ? $i18n.locale = Languages.GERMAN : $i18n.locale = Languages.ENGLISH; count++" :button-type="ButtonType.ACTIVE" :size="[150, 50]"
     :text="'count is: ' + count" />
    <p>
      Edit
      <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>

  <p>
    Check out
    <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank"
      >create-vue</a
    >, the official Vue + Vite starter
  </p>
  <p>
    Install
    <a href="https://github.com/johnsoncodehk/volar" target="_blank">Volar</a>
    in your IDE for a better DX
  </p>
  <p class="read-the-docs">Click on the Vite and Vue logos to learn more</p>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
