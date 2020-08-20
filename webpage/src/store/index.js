import Vue from 'vue'
import Vuex from 'vuex'
import Home from './index.json'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    host: "",
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
