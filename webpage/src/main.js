import Vue from 'vue'
import axios from "axios";
import App from './App.vue'
import store from './store'
import router from './router'
import VueAxios from "vue-axios";
import ElementUI from 'element-ui';
import VueCookies from 'vue-cookies'
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);
Vue.use(VueCookies);
Vue.use(VueAxios, axios);
Vue.config.productionTip = false

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
