<script setup lang="ts">
import {ref} from 'vue'
import {Languages} from "../../language/Languages";
import Button from "../basic/button/Button.vue";
import {ButtonType} from "../basic/button/ButtonType";
import Dropdown from "../basic/Dropdown.vue";

defineProps<{ msg: string }>()

const count = ref(0)

function consoleLog(log: any) {
  console.log(log)
}

</script>



<template>

  <Dropdown hint="Select an ODM" :options="['LUNAR', 'ROSE', 'PLANT', 'RESCUE', 'LILIE', 'NYA', 'AMOUNT', 'RADISH']" @onValueSelected="consoleLog" />
  <Button text="Click me" @buttonClick="count++" :button-type="ButtonType.DEFAULT" :text-size="[18, 500]"/>

  <h1>{{ $t('message.greeting') }}, {{$t('message.name')}}</h1>

  <div class="card">
    <button type="button" @click="$i18n.locale = Languages.GERMAN">count is {{ count }}</button>
    <Button text="Back to english" @buttonClick="$i18n.locale = Languages.ENGLISH" :button-type="ButtonType.DEFAULT" :text-size="[15, 500]"/>
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
