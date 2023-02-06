import { createRouter, createWebHistory } from 'vue-router'
import LandingPageView from "../components/views/LandingPageView.vue";
import store from "../store";
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
    component: () => import("../components/views/LoginView.vue"),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register-page',
    component: () => import("../components/views/RegisterView.vue"),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import("../components/views/Dashboard.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: '/experiment/:expId',
    name: "experiment-result",
    component: () => import('../components/views/ExperimentResultView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/experiment',
    name: "create-experiment-fallback",
    component: () => import('../components/views/CreateExperimentView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/create',
    name: "create-experiment",
    component: () => import('../components/views/CreateExperimentView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path:'/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../components/views/PageNotFound.vue'),
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})


router.beforeEach((to, from, next) => {
  if ((to.path === '/login' || to.path === '/register') && store.getters['auth/is_authenticated']) {
    next('/')
    return;
  }

  if (to.matched.some((record => record.meta.requiresAuth)) && !store.getters['auth/is_authenticated']) {
    next('/login')
    return;
  }

  next();
})


export default router