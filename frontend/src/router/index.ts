import { createRouter, createWebHistory } from 'vue-router'
import HelloWorld from "../components/views/HelloWorld.vue";
const routes = [
  {
    path: '/',
    name: 'hello-world',
    component: HelloWorld
  },
  {
    path:'/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../components/views/PageNotFound.vue')
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})
export default router