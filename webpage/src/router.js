import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'index',
      component: () => import(/* webpackChunkName: "tool" */ './views/Index.vue')
    },
    // route level code-splitting
    // which is lazy-loaded when the route is visited.
    {
      path: '/tools',
      alias: ['/tools/:tool'],
      name: 'tools',
      component: () => import(/* webpackChunkName: "tool" */ './views/Tool.vue')
    }
  ]
})
