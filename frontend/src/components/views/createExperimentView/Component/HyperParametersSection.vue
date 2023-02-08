<template>
  <div class="parameterSection">
    <div class="header">
      ODM Parameters
      <div style="border: 1px solid var(--color-lines); margin-top: .5vh; width: 12vw;"/>
    </div>
    <div v-if="visible" class="inputFields">
      <ParameterInputField v-for="param in parameters" :placeholder="param.name" @input-change="inputChange"
                           :parameter-id="param.id" :key="param.id" :ref="'inputRef' + param.id"/>
    </div>
  </div>
</template>

<script lang="ts">
import ParameterInputField from "./ParameterInputField.vue";
import {defineComponent} from "vue";
import {Hyperparameter} from "../../../../models/odm/Hyperparameter";
import {validateHyperparameterType} from "../../../../models/odm/HyperparameterType";

export default defineComponent({
  name: "HyperParametersSection",
  components: {ParameterInputField},
  data() {
    return {
      visible: true,
      parametersMap: new Map<number, Hyperparameter>()
    };
  },
  props: {
    parameters: {
      type: Array as () => Hyperparameter[],
      required: true
    }
  },
  watch: {
    parameters: function () {
      this.parameters.forEach(param => {
        this.parametersMap.set(param.id, param);
      })
    }
  },
  methods: {
    inputChange(value: string, parameterId: number) {
      (this.parametersMap.get(parameterId) as Hyperparameter).value = value;
      console.log(this.$refs[`inputRef${parameterId}`] as typeof ParameterInputField)
      if (!validateHyperparameterType(this.parametersMap.get(parameterId) as Hyperparameter)) {
        (this.$refs[`inputRef${parameterId}`] as typeof ParameterInputField)[0].wrongInput();
      } else {
        (this.$refs[`inputRef${parameterId}`] as typeof ParameterInputField)[0].correctInput();
      }
    }
  }
})

</script>

<style scoped>
.header {
  font-size: 1.2vw;
  padding: 5px;
  text-align: left;
  width: 98%;
  position: sticky;
  top: 0;
  background-color: var(--color-background);
}

.parameterSection {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: start;
}

.inputFields {
  width: 98%;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(8vw, 1fr));
  align-items: center;
  padding-left: 10px;
}


</style>