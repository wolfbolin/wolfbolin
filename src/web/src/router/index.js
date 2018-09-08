import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
// import Mobile from '@/components/Mobile'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    }
    // {
    //   path: '/mobile',
    //   name: 'Mobile',
    //   component: Mobile
    // }
  ]
})
