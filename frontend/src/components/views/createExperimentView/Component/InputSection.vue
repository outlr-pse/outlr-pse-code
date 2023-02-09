<template>
  <Card class="card">
    <div class="odmContainer">
      <div class="odm">
        <h3>
          {{ $t('message.experimentCreate.odm') }}
        </h3>
        <div style="border: 1px solid var(--color-lines);width: 20vw"/>
      </div>
      <Dropdown :options="odmNames" hint="Select ODM" class="dropdown" @onValueSelected="onODMSelection"/>
    </div>
    <div class="hyperparameter">
      <HyperParametersSection :parameters="hyperparameters" @checkData="$emit('checkData')"/>
    </div>
    <div class="subspace">
      <SubspaceSection @onInputChange="parseSubspaceLogic"></SubspaceSection>
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
import {SubspaceLogic} from "../../../../models/subspacelogic/SubspaceLogic";
import {Subspace} from "../../../../models/results/Subspace";
import {Literal} from "../../../../models/subspacelogic/Literal";
import {Operation} from "../../../../models/subspacelogic/Operation";
import {Operator} from "../../../../models/subspacelogic/Operator";

export default defineComponent({
  name: "InputSection",
  components: {HyperParametersSection, SubspaceSection, Dropdown, HyperParametersField, Card},
  data() {
    return {
      odmNames: [] as string[],
      odmMap: new Map<string, ODM>()
    }
  },
  props: {
    odms: {
      type: Array as () => ODM[],
      required: true
    },
    hyperparameters: {
      type: Array as () => Hyperparameter[],
      required: true
    }
  },
  watch: {
    odms: function (odms: ODM[]) {
      this.odmNames = []
      this.odmMap = new Map<string, ODM>()
      for (let odm of odms) {
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

      //Parse Subspace Logic
      let subspaceLogic = logic
      //Emit null when subspacelogic is invalid
      //Emit only when parsed successfully then its ensured the button can be clicked
      this.$emit("onSubspaceInput", subspaceLogic)
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
  width: 100%;
  font-weight: 600;
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