import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Building from '@/components/Building'

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/building',
      name: 'Building',
      component: Building
    }
  ]
})
