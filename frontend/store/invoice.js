export const state = () => ({
  invoices: [],
  invoiceById: null
})

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
          content: 'Ошибка загрузки чата!',
          red: true
        })
      })
  },

  async createInvoice({ dispatch }, invoiceForm) {
    return await this.$axios
      .post('/invoice/create/', invoiceForm)
      .then(res => {
        this.$router.push(`/invoice/${res.data._id}`)
        this.$toast.showMessage({
          content: 'Заявка успешно создана!',
          green: true
        })
        dispatch('fetchInvoices')
      })
      .catch(error => {
        // TEMPORARY BAD ASS SOLUTION, WILL BE FIXED
        switch (error.response.data[0].message) {
          case 'You have exceeded the lower limit':
            this.$toast.showMessage({
              content: 'Вы превысили нижний лимит объявления',
              red: true
            })
            break
          case 'You have exceeded the upper limit':
            this.$toast.showMessage({
              content: 'Вы превысили верхний лимит объявления',
              red: true
            })
            break
          case 'No such USDT on order':
            this.$toast.showMessage({
              content: 'Нет такого количества USDT в объявлении',
              red: true
            })
            break
          case 'Not enough USDT on wallet':
            this.$toast.showMessage({
              content: 'Недостаточно USDT на вашем кошельке',
              red: true
            })
            break
          case 'Wrong user role or invoice status':
            this.$toast.showMessage({
              content: 'Неправильный статус объявления',
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
          content: 'Заявка отменена!',
          green: true
        })
      })
      .catch(error => {
        this.$toast.showMessage({
          content: error.response.data[0].message,
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
          content: 'Ожидайте получения токенов',
          green: true
        })
      })
      .catch(error => {
        this.$toast.showMessage({
          content: error.response.data[0].message,
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
          content: 'Сделка завершена',
          green: true
        })
      })
      .catch(error => {
        this.$toast.showMessage({
          content: error.response.data[0].message,
          red: true
        })
      })
  }
}
