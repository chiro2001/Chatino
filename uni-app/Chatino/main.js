import Vue from 'vue'
import App from './App'

import utils from "@/utils/utils.js"
import config from "@/utils/config.vue"
import ws from "@/web/ws"
import jquery from "jQuery"

Vue.config.productionTip = false
Vue.prototype.utils = utils
Vue.prototype.ws = ws
Vue.prototype.config = config
Vue.prototype.$ = jquery

// Vue.prototype.wstask = undefined

App.mpType = 'app'

const app = new Vue({
	...App,
})
app.$mount()
