<template>
  <div id="app">
    <Topbar />
    <RouterView class="routerView" />
  </div>
</template>

<script lang="ts">

import Topbar from './components/topbar/Topbar.vue'
import { RouterView } from 'vue-router'

export default {

  components: {
    Topbar,
    RouterView
  },
  data () {
    return {
      loggedIn: false
    }
  }

}
</script>

<style scoped>

.routerView {
  height: var(--router-view-height);
  overflow: auto;
}
</style>
