<template>
  <div id="app">
    <TopBar/>
    <RouterView class="routerView"/>
  </div>
</template>

<script lang="ts">

import TopBar from "./components/TopBar.vue";

export default {
  data() {
    return {
      loggedIn: false
    }
  },

  components: {
    TopBar
  },

}
</script>


<style scoped>

.routerView {
  height: var(--router-view-height);
  overflow: auto;
}
</style>
