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
  async createInvoice({dispatch}, invoiceForm) {
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
        this.$toast.showMessage({
          content: error.response.data[0].message,
          red: true
        })
      })
  },
  async fetchInvoices({ commit }) {
    const { data } = await this.$axios.get('/invoice/')
    commit('setInvoices', data)
  },
  async fetchInvoiceById({ commit }, id) {
    const { data } = await this.$axios.get(`/invoice/${id}/`)
    // console.log(data)
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
  async confirmInvoice({dispatch}, id) {
    return await this.$axios.put(`/invoice/${id}/confirm/`).then(res => {
      console.log(res)
      dispatch('fetchInvoiceById', id)
      return true
    }).catch(error => {
      console.log(error)
      return false
    })
  }
}
