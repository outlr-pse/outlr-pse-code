<template>
    <div id="app">
        <Topbar />
        <RouterView class="routerView" />
    </div>
  <div id="app">
    <Topbar />
    <RouterView class="routerView" />
  </div>
</template>

<script lang="ts">

import Topbar from './components/topbar/Topbar.vue'
import { RouterView, useRoute, useRouter } from 'vue-router'
import { onBeforeMount } from 'vue'
import store from './store'
import { initialValidityCheck } from './api/AuthServices'
import { mapState } from 'vuex'

export default {
  setup () {
    const route = useRoute()
    const router = useRouter()
    const rerouteIfNecessary = async () => {
      if ((route.path === 'login' || route.path === 'register') && store.getters['auth/isAuthenticated']) {
        await router.push('/')
      }

      if (route.meta.requiresAuth && !store.getters['auth/isAuthenticated']) {
        await router.push('/login')
      }
    }

    onBeforeMount(async () => {
      await initialValidityCheck()
      await router.isReady()
      await rerouteIfNecessary()
    })

    store.subscribeAction({
      after: async (action, state) => {
        if (action.type === 'auth/unsetAuthenticated') {
          await rerouteIfNecessary()
        }
      }
    })
  },
  data () {
    return {
      loggedIn: false
    }
  },
  components: {
    Topbar,
    RouterView
  }
}
</script>

<style scoped>

.routerView {
    height: var(--router-view-height);
    overflow: auto;
}
</style>
