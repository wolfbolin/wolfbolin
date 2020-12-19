import Vue from 'vue'
import Vuex from 'vuex'
import Tool from './tool.json'
import Home from './index.json'
import Album from "./album.json";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        host: "",
        user_token: "",
        home_data: Home,
        tool_data: Tool,
        blog_data: null,
        album_list: Album,
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
