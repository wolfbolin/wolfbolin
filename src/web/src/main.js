// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import axios from 'axios';
import router from './router'
import VueI18n from 'vue-i18n'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.config.productionTip = false;
Vue.prototype.$http = axios;

// 引入多语言支持
Vue.use(VueI18n);
const i18n = new VueI18n({
  locale: 'zh-CN',    // 语言标识, 通过切换locale的值来实现语言切换,this.$i18n.locale
  messages: {
    'zh-CN': require('./assets/common/lang/zh-cn'),
    'en-US': require('./assets/common/lang/en-us'),
  }
});

Vue.use(ElementUI);

new Vue({
  el: '#app',
  router,
  i18n,
  components: { App },
  template: '<App/>'
});
