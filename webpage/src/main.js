import Vue from 'vue'
import axios from 'axios'
import App from './App.vue'
import store from './store'
import router from './router'
import VueAxios from 'vue-axios'
import {
    Row,
    Col,
    Tag,
    Card,
    Button,
    Carousel,
    CarouselItem
} from 'element-ui';

Vue.component(Row.name, Row);
Vue.component(Col.name, Col);
Vue.component(Tag.name, Tag);
Vue.component(Card.name, Card);
Vue.component(Button.name, Button);
Vue.component(Carousel.name, Carousel);
Vue.component(CarouselItem.name, CarouselItem);

Vue.use(VueAxios, axios);
Vue.config.productionTip = false;

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');
