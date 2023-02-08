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

        <p>{{ experimentName }}</p>
      </div>
      <Card style="width: 30vw; display: flex; flex-direction: column; ">
        <div class="Dataset">
          <h3>Dataset</h3>
          <input type="file" ref="fileInput" @change="onDataSetFileChange"/>

        </div>
        <div class="Groundtruth file">
          <h3>Groundtruth</h3>
          <input style="" type="file" ref="fileInput" @change="onGroundTruthFileChange">
        </div>
      </Card>

        <img :src="preview"/> <!-- adfasdfassssssssssssssssssssssssssssssssssssssss   TODO -->

    </div>
    <div class="right-half">
      <Card style="width: 40vw; display: flex; flex-direction: column;">
        <div class="ODM">
          <h2>ODM</h2>
          <Dropdown>

          </Dropdown>
        </div>
        <div class="Hyperparameter">
          <h3>Hyperparameter</h3>
        </div>
        <div class="SubspaceLogic">
          <h3>SubspaceLogic</h3>
        </div>
      </Card>
    </div>
  </div>
</template>

<script lang="ts">
import Card from "../basic/Card.vue";
import {defineComponent} from "vue";
import Dropdown from "../basic/Dropdown.vue";

export default defineComponent({
  name: "CreateExperimentView",
  components: {Dropdown, Card},
  data() {
    return {
      editableName: 'Experiment 3425',
      experimentName: 'Experiment 3425',
      preview: "null",
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
    }
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

.Dataset, .Groundtruth {
  width: 100%;
  height: 50%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin: 25px;
}

.ODM {
  height: 27%;
}

.Hyperparameter {
    height: 27%;
}

.SubspaceLogic {
    height: 27%;
}

</style>