import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VeLine from 'v-charts/lib/line.common.min'
Vue.prototype.$axios = axios
Vue.component(VeLine.name,VeLine)
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
