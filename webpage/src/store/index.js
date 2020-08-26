import Vue from 'vue'
import Vuex from 'vuex'
import Home from './index.json'
import Tool from './tool.json'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        host: "",
        home_data: Home,
        tool_data: Tool,
        blog_data: null,
        user_token: ""
    },
    mutations: {
        setData(state, param) {
            let val = param.val;
            if (typeof param.val == "object") {
                val = JSON.stringify(val);
            } else if (typeof param.val == "string") {
                val = `"${val}"`
            }
            eval(`state.${param.key}=${val}`);
        }
    },
    actions: {},
    modules: {}
})
