import Vue from 'vue'
import Vuex from 'vuex'
import Index_data from './assets/index'
import Title_data from './assets/title'
import Tool_data from './assets/tool_box'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        host: 'http://127.0.0.1:5000',
        blog_selection: null,
        index_data: Index_data,
        title_data: Title_data,
        tool_box: Tool_data,
        user_role: "",
    },
    mutations: {},
    actions: {}
})
