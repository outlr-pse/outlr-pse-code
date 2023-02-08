<template>
  <div class="Uploadfile">
    <h3>{{ inputName }}</h3>
    <input class="input" type="file" ref="file Input" @change="onFileChange">
  </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
  name: "UploadFileField",
  methods: {
    onFileChange(e: any) {
      const file = e.target.files[0];
      this.$emit("file-uploaded", file)
    },
  },
  props: {
    inputName: {
      type: String,
      default: "Upload a file",
      required: false
    }
  },

})
</script>

<style scoped>
.Uploadfile {
  width: 100%;
  height: 50%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin: 25px;
}

.input {

}
</style>