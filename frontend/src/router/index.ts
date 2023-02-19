import { createRouter, createWebHistory } from 'vue-router'
import LandingPageView from "../components/views/LandingPageView.vue";
import store from "../store";
import { initialValidityCheck } from "../api/AuthServices";
import { storage } from "../api/APIRequests";
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
    component: () => import("../components/views/LoginView/LoginView.vue"),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register-page',
    component: () => import("../components/views/RegisterView/RegisterView.vue"),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import("../components/views/dashboard/Dashboard.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: '/experiment/:expId',
    name: "experiment-result",
    component: () => import('../components/views/experimentresult/ExperimentResultView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/experiment',
    name: "create-experiment-fallback",
    component: () => import('../components/views/createExperimentView/CreateExperimentView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/create',
    name: "create-experiment",
    component: () => import('../components/views/createExperimentView/CreateExperimentView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path:'/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../components/views/PageNotFound.vue'),
  },
]
const router = createRouter({
  history: createWebHistory(),
  routes
})


router.beforeEach(async (to, from, next) => {
  if ((to.path === '/login' || to.path === '/register') && store.getters['auth/isAuthenticated']) {
    await initialValidityCheck()
    if (store.getters['auth/isAuthenticated']) {
      next('/')
    }
    return;
  }

  if (to.matched.some((record => record.meta.requiresAuth)) && (!storage.getItem("access_token") || !store.getters['auth/isAuthenticated'])) {
    next('/login')
    return;
  }

  next();
})


export default router