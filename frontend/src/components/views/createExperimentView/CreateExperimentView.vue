<template>
  <div class="container">
    <div class="left-half">
      <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
        <div style="display: flex; align-items: center;">
          <p contenteditable="true" @input="onExperimentInput" class="exp-name"> {{ editableName }} </p>
          <i class="material-icons md-light" style="margin-left: auto; color: var(--color-stroke);
           align-self: flex-end; margin-bottom: 15px">border_color</i>
        </div>
        <div style="width: 30vw;  height: 2px;  background-color: var(--color-lines);  margin: 0 10px;"></div>

        <p>{{ experimentName }}</p> <!-- adfasdfassssssssssssssssssssssssssssssssssssssss   TODO -->
      </div>
      <Card style="width: 30vw; display: flex; flex-direction: column; ">
        <h2> Upload Files</h2>
        <UploadFileField input-name="Dashboard" />
        <UploadFileField input-name="Groundtruth" />
      </Card>
            <Button class="button" text="Create Experiment" :size="[250,60]"></Button>
    </div>
    <div class="right-half">
      <InputSection @onODMSelection="onODMSelection"  :hyperparameters="hyperparameters" v-bind:odms="odms" class="inputSection"/>
    </div>

  </div>
</template>

<script lang="ts">
import Card from "../../basic/Card.vue";
import {defineComponent} from "vue";
import Dropdown from "../../basic/Dropdown.vue";
import UploadFileField from "./Component/UploadFileField.vue";
import HyperParametersField from "./Component/HyperParametersSection.vue";
import {Hyperparameter} from "../../../models/odm/Hyperparameter";
import {HyperparameterType} from "../../../models/odm/HyperparameterType";
import ODMSection from "./Component/InputSection.vue";
import {ODM} from "../../../models/odm/ODM";
import {requestODM, requestODMNames} from "../../../api/APIRequests";
import Button from "../../basic/button/Button.vue";
import InputSection from "./Component/InputSection.vue";

export default defineComponent({
  name: "CreateExperimentView",
  components: {InputSection, Button, ODMSection, HyperParametersField, UploadFileField, Dropdown, Card},
  data() {
    return {
      editableName: 'Experiment 3425',
      experimentName: 'Experiment 3425',
      preview: "null",
      odms: [] as ODM[],
      hyperparameters: [] as Hyperparameter[],
      selectedODM: null as ODM | null
    }
  },
  methods: {
    onExperimentInput(event: any) {
      this.experimentName = event.target.textContent;
    },
    onDataSetFileChange(e: any) {
      const file= e.target.files[0];
    },
    onGroundTruthFileChange(e: any) {
      const file= e.target.files[0];
      this.preview = URL.createObjectURL(file);

      // Do something with the file
    },
    async onODMSelection(odm: ODM) {
      let response = await requestODM(odm.id)
      this.hyperparameters = []
      for (let param of response.data) {
        this.hyperparameters.push(Hyperparameter.fromJSON(param))
      }
      this.selectedODM = odm
      this.selectedODM.hyperParameters = this.hyperparameters

    },
  },
  async mounted() {
    let response = await requestODMNames()
    let odms = []
    for(let odm of response.data) {
      odms.push(ODM.fromJSON(odm))
    }
    this.odms = odms
  }
})
</script>

<style scoped>
.container {
  display: flex;
  height: 100%;
}


.left-half {
  height: 100%;
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.right-half {
  height: 100%;
  width: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.exp-name {
  display: inline;
  outline: none;
  font-size: 40px;
  font-weight: 500;
  width: 25vw;
  height: 50px;
  overflow-x: hidden;
  overflow-y: hidden;
  text-align: center;
  white-space: nowrap;
}

h3 {
  margin: 5px;
}

.button {
  margin-top: 20px;
}

.inputSection {
  margin-top: 8vh;
}

</style>