<template>
  <div id="app">
    <Topbar/>
    <RouterView class="routerView"/>
  </div>
</template>

<script lang="ts">

import Topbar from "./components/topbar/Topbar.vue";
import {RouterView} from "vue-router";

export default {
  data() {
    return {
      loggedIn: false
    }
  },

  components: {
    Topbar,
    RouterView
  },

}
</script>


<style scoped>

.routerView {
  height: var(--router-view-height);
  overflow: auto;
}
</style>
