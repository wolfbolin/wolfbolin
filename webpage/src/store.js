import Vue from 'vue'
import Vuex from 'vuex'
import Index_data from './assets/index'
import Title_data from './assets/title'
import Box_list from './assets/tool_box'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        host: 'http://127.0.0.1:5000',
        blog_selection: null,
        index_data: Index_data,
        title_data: Title_data,
        box_list: Box_list,
        user_role: "",
    },
    mutations: {},
    actions: {}
})
