import Vue from 'vue'
import Vuex from 'vuex'
import Index_data from './assets/index'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        host: 'http://127.0.0.1:5000',
        blog_selection: null,
        index_data: Index_data
    },
    mutations: {},
    actions: {}
})
