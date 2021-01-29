import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import(/* webpackChunkName: "home" */ '../views/Home.vue')
    },
    {
        path: '/album',
        alias: ['/album/:box', '/album/:box/:tool'],
        name: 'Album',
        component: () => import(/* webpackChunkName: "home" */ '../views/Album.vue')
    },
    {
        path: '/tools',
        alias: ['/tools/:box', '/tools/:box/:tool'],
        name: 'Tool',
        component: () => import(/* webpackChunkName: "home" */ '../views/Tool.vue')
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
