import Vue           from 'vue'
import VueNativeSock from 'vue-native-websocket'

Vue.use(VueNativeSock,`${process.env.API_WS_URL}invoice/ws/${this.invoice.chat_id}/`)
