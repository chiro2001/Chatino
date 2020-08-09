import App from './App.vue'
import MuseUI from 'muse-ui';
import Helpers from 'muse-ui/lib/Helpers';
import 'muse-ui/dist/muse-ui.css';
import Toast from 'muse-ui-toast';
import 'typeface-roboto'

// 把PageDrawer注册到全局
// import PageDrawer from "./components/pageComponents/PageDrawer.vue"

// 为什么放下来才不会有错误？是否为import顺序的影响？
import Vue from 'vue'

Vue.use(Helpers);
Vue.use(MuseUI);
Vue.use(Toast);
// Vue.use(PageDrawer);
// Vue.component('page-drawer', PageDrawer);

Vue.config.productionTip = false

let vm = new Vue({
  render: h => h(App),
  create: function() {
    console.log('paike-admin has launched.')
  }
});

vm.$mount('#app');