import { createRouter, createWebHistory } from 'vue-router'
import LandingPageView from '../components/views/LandingPageView.vue'
import store from '../store'
import { initialValidityCheck } from '../api/AuthServices'
import storage from '../api/Storage'
const routes = [
  {
    path: '/',
    name: 'landing-page',
    component: LandingPageView,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'login-page',
    component: async () => await import('../components/views/LoginView/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register-page',
    component: async () => await import('../components/views/RegisterView/RegisterView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: async () => await import('../components/views/dashboard/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/experiment/:expId',
    name: 'experiment-result',
    component: async () => await import('../components/views/experimentresult/ExperimentResultView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/experiment',
    name: 'create-experiment-fallback',
    component: async () => await import('../components/views/createExperimentView/CreateExperimentView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/create',
    name: 'create-experiment',
    component: async () => await import('../components/views/createExperimentView/CreateExperimentView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: async () => await import('../components/views/PageNotFound.vue')
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  // eslint-disable-next-line
  if ((to.path === '/login' || to.path === '/register') && store.getters['auth/isAuthenticated']) {
    await initialValidityCheck()
    // eslint-disable-next-line
    if (store.getters['auth/isAuthenticated']) {
      next('/')
    }
    return
  }

  // eslint-disable-next-line
  if (to.matched.some((record => record.meta.requiresAuth)) && (!storage.getItem("access_token") || !store.getters['auth/isAuthenticated'])) {
    next('/login')
    return
  }
  next()
})

export default router
