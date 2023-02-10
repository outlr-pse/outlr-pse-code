<template>
  <div class="container">
    <div class="left-half">
      <div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
        <div style="display: flex; align-items: center;">
          <p contenteditable="true" @input="onExperimentInput" class="exp-name"> {{ editableName }} </p>
          <i class="material-icons md-light" style="margin-left: auto; color: var(--color-stroke);
           align-self: flex-end; margin-bottom: 10px; font-size: 20px">border_color</i>
        </div>
        <div style="width: 30vw;  height: 2px;  background-color: var(--color-lines); margin-bottom: 35px"></div>

        <!--        <div style="height: 50px">{{ experimentName }}</div> &lt;!&ndash; adfasdfassssssssssssssssssssssssssssssssssssssss   TODO &ndash;&gt;-->
      </div>
      <Card style="width: 30vw; display: flex; flex-direction: column; ">
        <h3 style="font-size: 27px"> Upload Files</h3>
        <!--         <div style="width: 150px;  height: 2px;  background-color: var(&#45;&#45;color-lines);  margin: 0 7px; text-align: center"></div>-->
        <UploadFileField :input-name="$t('message.experimentCreate.dataset')" @file-uploaded="setDataset"/>
        <UploadFileField style="margin-bottom: 15px" :input-name="$t('message.experimentCreate.groundtruth')" @file-uploaded="setGroundtruth"/>
      </Card>
      <Button :button-type="buttonType" style="margin-top: 45px;" class="button" text="Create Experiment"
              :size="[250,60]" :text-size="[22,600]" @buttonClick="createExperiment"/>
    </div>
    <div class="right-half">
      <InputSection @onODMSelection="onODMSelection" :hyperparameters="hyperparameters" v-bind:odms="odms"
                    class="inputSection" @checkData="checkRequiredData" @onSubspaceInput="setSubspaceLogic"/>
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
import {validateHyperparameterType} from "../../../models/odm/HyperparameterType";
import ODMSection from "./Component/InputSection.vue";
import {ODM} from "../../../models/odm/ODM";
import {requestODM, requestODMNames, sendExperiment} from "../../../api/APIRequests";
import Button from "../../basic/button/Button.vue";
import InputSection from "./Component/InputSection.vue";
import {ButtonType} from "../../basic/button/ButtonType";
import {SubspaceLogic} from "../../../models/subspacelogic/SubspaceLogic";
import {Experiment} from "../../../models/experiment/Experiment";

export default defineComponent({
  name: "CreateExperimentView",
  components: {InputSection, Button, ODMSection, HyperParametersField, UploadFileField, Dropdown, Card},
  data() {
    return {
      editableName: 'new Experiment',
      experimentName: 'new Experiment',
      odms: [] as ODM[],
      hyperparameters: [] as Hyperparameter[],
      buttonType: ButtonType.DISABLED,


      selectedODM: null as ODM | null,
      dataset: null as File | null,
      groundtruth: null as File | null,
      subspaceLogic: null as SubspaceLogic | null,

    }
  },
  methods: {
    onExperimentInput(event: any) {
      this.experimentName = event.target.textContent;
    },
    async onODMSelection(odm: ODM) {
      let response = await requestODM(odm.id)
      this.hyperparameters = []
      for (let param of response.data) {
        this.hyperparameters.push(Hyperparameter.fromJSON(param))
      }
      this.selectedODM = odm
      this.selectedODM.hyperParameters = this.hyperparameters
      this.checkRequiredData()
    },
    setDataset(dataset: File) {
      this.dataset = dataset
      this.checkRequiredData()
    },
    setGroundtruth(groundtruth: File) {
      this.groundtruth = groundtruth
    },
    setSubspaceLogic(subspaceLogic: SubspaceLogic) {
      this.subspaceLogic = subspaceLogic
      this.checkRequiredData()
    },
    checkRequiredData() {
      if (this.selectedODM === null) {
        this.buttonType = ButtonType.DISABLED
        console.log("no odm selected")
        return
      }
      for (let param of this.selectedODM.hyperParameters) {
        if (!param.optional && param.value === "") {
          this.buttonType = ButtonType.DISABLED
          console.log("no value for " + param.name)
          return
        }
        if (!validateHyperparameterType(param) && param.value !== "") {
          this.buttonType = ButtonType.DISABLED
          console.log("wrong type for " + param.name)
          return
        }
      }
      if(this.dataset === null){
         this.buttonType = ButtonType.DISABLED
        console.log("no dataset")
         return
      }
      if(this.subspaceLogic === null) {
        this.buttonType = ButtonType.DISABLED
        console.log("no subspace logic")
        return
      }
      this.buttonType = ButtonType.ACTIVE
    },
    async createExperiment() {
      let experiment = new Experiment(
          this.experimentName,
          this.dataset?.name as string,
          this.dataset as File,
          this.groundtruth as File,
          this.selectedODM as ODM,
          this.subspaceLogic as SubspaceLogic
      )
      let response = await sendExperiment(experiment)
      if (response.status === 200) {
        //this.$router.push('/dashboard')
      } else {
        console.log(response)
      }
    }
  },
  async mounted() {
    let response = await requestODMNames()
    let odms = []
    for (let odm of response.data) {
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
  margin-bottom: 3px;
}

h2, h3 {
  margin: 5px;

}

.button {
  margin-top: 20px;
}

.inputSection {
  margin-top: 8vh;
}

</style>