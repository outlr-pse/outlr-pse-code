<template>
  <div id="app">
    <Topbar/>
    <RouterView class="routerView"/>
  </div>
</template>

<script lang="ts">
import Topbar from './components/views/Topbar.vue';
import Button from "./components/basic/button/Button.vue";
export default {
  components: {
    Topbar,
    Button
  },

}
</script>