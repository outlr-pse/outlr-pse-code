<template>
  <div id="app">
    <RouterView class="routerView"/>
  </div>
</template>

<script lang="ts">
import {RouterView} from "vue-router";

export default {
  data() {
    return {
      loggedIn: false
    }
  },

  components: {
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
