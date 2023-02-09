<template>
  <div class="parameterSection">
    <div class="header">
      ODM Parameters
      <span class="material-icons md-dark icon" @mouseenter="showTip = true" @mouseleave="showTip = false">
        information
      </span>
      <transition name="fade">
        <Card class="card" v-if="showTip" @mouseleave="showTip = false" @mouseenter="showTip = true">
          {{ $t('message.experimentCreate.paramHint') }}
        </Card>
      </transition>
      <div style="border: 1px solid var(--color-lines); margin-top: .5vh; width: 12vw;"/>
    </div>
    <div v-if="visible" class="inputFields">
      <ParameterInputField v-for="param in parameters" :placeholder="param.name" @input-change="inputChange"
                           :parameter-id="param.id" :key="param.id" :ref="'inputRef' + param.id"
                           :optional="param.optional" @checkData="this.$emit('checkData')"/>
    </div>
  </div>
</template>

<script lang="ts">
import ParameterInputField from "./ParameterInputField.vue";
import {defineComponent} from "vue";
import {Hyperparameter} from "../../../../models/odm/Hyperparameter";
import {validateHyperparameterType} from "../../../../models/odm/HyperparameterType";
import Card from "../../../basic/Card.vue";

export default defineComponent({
  name: "HyperParametersSection",
  components: {Card, ParameterInputField},
  data() {
    return {
      visible: true,
      parametersMap: new Map<number, Hyperparameter>(),
      showTip: false
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
      let param = this.parametersMap.get(parameterId) as Hyperparameter;
      if (!validateHyperparameterType(param)&& param.value !== "") {
        (this.$refs[`inputRef${parameterId}`] as typeof ParameterInputField)[0].wrongInput();
      } else if (!param.optional) {
        (this.$refs[`inputRef${parameterId}`] as typeof ParameterInputField)[0].optionalInput();
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

.icon {
  color: var(--color-text);
  width: 24px;
  font-size: 18px;
}

.icon:hover {
  cursor: pointer;
}

.card {
  position: absolute;
  top: 70%;
  left: 25%;
  right: 0;
  width: 15vw;
  height: max-content;
  background-color: rgb(47, 41, 58);
  z-index: 100;
  border-radius: 12px;
  border: 1px solid var(--color-stroke);
  font-size: 14px;
  white-space: break-spaces;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}


</style>