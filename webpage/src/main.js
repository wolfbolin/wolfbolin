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
    Tabs,
    Card,
    Form,
    Input,
    Alert,
    Table,
    Button,
    Switch,
    TabPane,
    Divider,
    Timeline,
    Carousel,
    Collapse,
    FormItem,
    Breadcrumb,
    TableColumn,
    TimelineItem,
    CarouselItem,
    CollapseItem,
    BreadcrumbItem,
} from 'element-ui';

Vue.component(Row.name, Row);
Vue.component(Col.name, Col);
Vue.component(Tag.name, Tag);
Vue.component(Tabs.name, Tabs);
Vue.component(Card.name, Card);
Vue.component(Form.name, Form);
Vue.component(Input.name, Input);
Vue.component(Alert.name, Alert);
Vue.component(Table.name, Table);
Vue.component(Button.name, Button);
Vue.component(Switch.name, Switch);
Vue.component(TabPane.name, TabPane);
Vue.component(Divider.name, Divider);
Vue.component(Timeline.name, Timeline);
Vue.component(Carousel.name, Carousel);
Vue.component(Collapse.name, Collapse);
Vue.component(FormItem.name, FormItem);
Vue.component(Breadcrumb.name, Breadcrumb);
Vue.component(TableColumn.name, TableColumn);
Vue.component(TimelineItem.name, TimelineItem);
Vue.component(CarouselItem.name, CarouselItem);
Vue.component(CollapseItem.name, CollapseItem);
Vue.component(BreadcrumbItem.name, BreadcrumbItem);

Vue.use(VueAxios, axios);
Vue.config.productionTip = false;

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');
