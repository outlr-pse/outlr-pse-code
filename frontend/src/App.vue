<template>
  <div id="app">
    <Topbar/>
    <RouterView class="routerView"/>
  </div>
</template>

<script lang="ts">

import Topbar from "./components/topbar/Topbar.vue";
import {RouterView} from "vue-router";
import "vue-router/dist/vue-router";
import {defineComponent} from "vue";
import store from "./store";
import {requestTokenIdentity, storage} from "./api/APIRequests";

export default defineComponent({
  data() {
    return {
      loggedIn: false,
      intervalID: null as any

    }
  },
  mounted() {
    this.intervalID = setInterval(this.checkAuth, 1000)
  },
  beforeUnmount() {
    clearInterval(this.intervalID)
  },
  methods: {
    async checkAuth() {
      if (this.$route.meta.requiresAuth) {
        console.log("Checking auth")
        let responseJson = await requestTokenIdentity()
        if (responseJson != null && "username" in responseJson && "access_token" in responseJson) {
          await store.dispatch("auth/setAuthenticated", responseJson.username)
        } else {
          console.log("Unsetting auth")
          await store.dispatch("auth/unsetAuthenticated")
          this.$router.push("/")
        }
      }
    }
  },
  components: {
    Topbar,
    RouterView
  },

})
</script>


<style scoped>

.routerView {
  height: var(--router-view-height);
  overflow: auto;
}
</style>
