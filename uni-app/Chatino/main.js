import Vue from 'vue'
import App from './App'

import utils from "@/utils/utils.js"
import config from "@/utils/config.vue"
import ws from "@/web/ws"
import jquery from "jQuery"
import InDB from "indb"
import { Remarkable } from "remarkable"

Vue.config.productionTip = false
Vue.prototype.utils = utils
Vue.prototype.ws = ws
Vue.prototype.config = config
Vue.prototype.$ = jquery
Vue.prototype.md = new Remarkable(config.data.mdOptions)

const idb = new InDB({
	name: 'chatino',
	version: 1,
	stores: [{
		name: 'user',
		keyPath: 'id',
	}, ],
})

Vue.prototype.idb = idb

// Vue.prototype.wstask = undefined

App.mpType = 'app'

const app = new Vue({
	...App,
})
app.$mount()
