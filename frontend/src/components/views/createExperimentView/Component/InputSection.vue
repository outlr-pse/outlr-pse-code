<template>
  <Card class="card">
    <div class="odmContainer">
      <div class="odm">
        <h2>
          {{ $t('message.experimentCreate.odm') }}
        </h2>
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
import Card from '../../../basic/Card.vue'
import { Hyperparameter } from '../../../../models/odm/Hyperparameter'
import { defineComponent } from 'vue'
import Dropdown from '../../../basic/Dropdown.vue'
import { ODM } from '../../../../models/odm/ODM'
import SubspaceSection from './SubspaceSection.vue'
import HyperParametersSection from './HyperParametersSection.vue'
import { parseSubspaceLogic } from '../../../../logic/subspace_logic_parser/SubspaceLogicParser'

export default defineComponent({
  name: 'InputSection',
  components: { HyperParametersSection, SubspaceSection, Dropdown, Card },
  data () {
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
      for (const odm of odms) {
        this.odmMap.set(odm.name, odm)
        this.odmNames.push(odm.name)
      }
      this.odmNames.sort()
    }
  },
  methods: {
    onODMSelection (odmName: string) {
      this.$emit('onODMSelection', this.odmMap.get(odmName))
    },
    parseSubspaceLogic (logic: string) {
      try {
        const subspaceLogic = parseSubspaceLogic(logic)
        this.$emit('onSubspaceInput', subspaceLogic)
      } catch (e) {
        this.$emit('onSubspaceInput', null)
      }
    }
  }
})
</script>

<style scoped>
.card {
  width: 40vw;
  height: 750px;
}

.odm {
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
