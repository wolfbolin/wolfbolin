import Vue from 'vue'
import Vuex from 'vuex'
import Home from './index.json'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    host: 'http://127.0.0.1:12880',
    home_data: Home,
    blog_data: null
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
