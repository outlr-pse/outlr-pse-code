<template>
  <Card class="card">
    <div class="odmContainer">
      <div class="odm">
        Outlier Detection Method
        <div style="border: 1px solid var(--color-lines); margin-top: .5vh"/>
      </div>
      <Dropdown :options="odmNames" hint="Select ODM" class="dropdown" @onValueSelected="onODMSelection"/>
    </div>
    <div class="hyperparameter">
      <HyperParametersSection :parameters="hyperparameters" @checkData="this.$emit('checkData')"/>
    </div>
    <div class="subspace">
      <SubspaceSection @onInputChange="parseSubspaceLogic" ></SubspaceSection>
    </div>
  </Card>
</template>

<script lang="ts">
import Card from "../../../basic/Card.vue";
import {Hyperparameter} from "../../../../models/odm/Hyperparameter";
import {defineComponent} from "vue";
import HyperParametersField from "./HyperParametersSection.vue";
import Dropdown from "../../../basic/Dropdown.vue";
import {ODM} from "../../../../models/odm/ODM";
import SubspaceSection from "./SubspaceSection.vue";
import HyperParametersSection from "./HyperParametersSection.vue";

export default defineComponent({
  name: "InputSection",
  components: {HyperParametersSection, SubspaceSection, Dropdown, HyperParametersField, Card},
  data(){
    return {
      odmNames: [] as string[],
      odmMap: new Map<string, ODM>()
    }
  },
  props:{
    odms:{
      type: Array as () => ODM[],
      required: true
    },
    hyperparameters:{
      type: Array as () => Hyperparameter[],
      required: true
    }
  },
  watch: {
    odms: function (odms: ODM[]) {
      this.odmNames = []
      this.odmMap = new Map<string, ODM>()
      for(let odm of odms){
        this.odmMap.set(odm.name, odm)
        this.odmNames.push(odm.name)
      }
      this.odmNames.sort()
    }
  },
  methods: {
    onODMSelection(odmName: string) {
      this.$emit("onODMSelection", this.odmMap.get(odmName))
    },
    parseSubspaceLogic(logic: string) {
      let subspaceLogic = logic
      this.$emit("subspaceLogic", subspaceLogic)
    }
  }
})
</script>

<style scoped>
.card {
  width: 40vw;
  height: 75vh;
}

.odm {
  font-size: 1.2vw;
  padding: 5px;
  text-align: left;
  width: 17vw;
}
.dropdown {
  margin: 15px;
  z-index: 100;
}
.odmContainer {
  height: 20%;
}

.hyperparameter {
  height: 48%;
  overflow: auto;
}

.subspace {
  height: 30%;
}


</style>