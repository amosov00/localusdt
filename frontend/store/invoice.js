export const state = () => ({
  invoices: [],
  invoiceById: null
})
let socketPing = null

export const getters = {
  invoices: s => s.invoices,
  invoiceById: s => s.invoiceById
}

export const mutations = {
  setInvoices: (state, payload) => {
    state.invoices = payload
  },
  setInvoiceById: (state, payload) => {
    state.invoiceById = payload
  }
}

export const actions = {
  async getChatroomMessages({}, chat_id) {
    return this.$axios.get(`/invoice/chatroom/${chat_id}/`)
      .then(res => res.data.messages)
      .catch((e) => {
        console.log(e)
        this.$toast.showMessage({
          content: $nuxt.$t('store.chatError'),
          red: true
        })
      })
  },

  async createInvoice({ dispatch }, invoiceForm) {
    delete invoiceForm.chatText
    return await this.$axios.post('/invoice/create/', invoiceForm)
      .then(res => {
        const ws = new WebSocket(`${process.env.API_WS_URL}invoice/ws/${res.data.chat_id}/`)
          ws.onopen = () => {
            console.log('SOCKET');
            ws.send(invoiceForm.chatText)
            console.log('SOCKET FIRST SEND');
            setTimeout(() => {
              socketPing = setInterval(() => {
                this.socket.send('');
              }, 50000);
            }, 2000);
          }

          ws.onclose = async (event) => {
            clearInterval(socketPing);
          };
        this.$toast.showMessage({
          content: $nuxt.$t('store.invoiceCreate'),
          green: true
        })
        dispatch('fetchInvoices')
        console.log('push router');
        this.$router.push(`/invoice/${res.data._id}`)
        return true
      })
      .catch(error => {
        // TEMPORARY BAD ASS SOLUTION, WILL BE FIXED
        switch (error.response.data[0].message) {
          case 'You have exceeded the lower limit':
            this.$toast.showMessage({
              content: $nuxt.$t('store.statusError1'),
              red: true
            })
            break
          case 'You have exceeded the upper limit':
            this.$toast.showMessage({
              content: $nuxt.$t('store.statusError2'),
              red: true
            })
            break
          case 'No such USDT on order':
            this.$toast.showMessage({
              content: $nuxt.$t('store.statusError3'),
              red: true
            })
            break
          case 'Not enough USDT on wallet':
            this.$toast.showMessage({
              content: $nuxt.$t('store.statusError4'),
              red: true
            })
            break
          case 'Wrong user role or invoice status':
            this.$toast.showMessage({
              content: $nuxt.$t('store.statusError5'),
              red: true
            })
            break
        }
      })
  },
  async fetchInvoices({ commit }) {
    const { data } = await this.$axios.get('/invoice/')
    commit('setInvoices', data)
  },
  async fetchInvoiceById({ commit }, id) {
    const { data } = await this.$axios.get(`/invoice/${id}/`, { progress: false })
    commit('setInvoiceById', data)
  },
  async cancelInvoice({}, id) {
    return this.$axios
      .put(`/invoice/${id}/cancel/`)
      .then(() => {
        this.$router.push('/')
        this.$toast.showMessage({
          content: $nuxt.$t('store.invoiceCancel'),
          green: true
        })
      })
      .catch(error => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.invoiceCancelError'),
          red: true
        })
      })
  },
  async confirmInvoice({ dispatch }, id) {
    await this.$axios
      .put(`/invoice/${id}/confirm/`)
      .then(res => {
        dispatch('fetchInvoiceById', id)
        dispatch('fetchUser', null, { root: true })
        this.$toast.showMessage({
          content: $nuxt.$t('store.waitToken'),
          green: true
        })
      })
      .catch(error => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.invoiceConfirmError'),
          red: true
        })
      })
  },
  async transferInvoice({ dispatch }, id) {
    await this.$axios
      .put(`/invoice/${id}/transfer/`)
      .then(res => {
        dispatch('fetchInvoiceById', id)
        dispatch('fetchUser', null, { root: true })
        this.$toast.showMessage({
          content: $nuxt.$t('store.invoiceEnd'),
          green: true
        })
      })
      .catch(error => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.invoiceTransferError'),
          red: true
        })
      })
  }
}
