export const state = () => ({
  orders: [],
  orderById: null
})

export const getters = {
  orders: s => s.orders,
  orderById: s => s.orderById,
  buyOrders: s => s.orders.filter(order => order.type === 1),
  sellOrders: s => s.orders.filter(order => order.type === 2)
}

export const mutations = {
  setOrders: (state, payload) => (state.orders = payload),
  setOrderById: (state, payload) => (state.orderById = payload)
}

export const actions = {
  async fetchOrders({ commit }, query) {
    const { data } = await this.$axios.get(`/order/?limit=${query.limit}&${query.type ? `ad_type=${query.type}` : ''}`)
    commit('setOrders', data)
  },
  async fetchOrderById({ commit }, id) {
    const { data } = await this.$axios.get(`/order/${id}`)
    commit('setOrderById', data)
  },
  async searchOrders({commit}, params) {
    const { data } = await this.$axios.get(`/order/?ad_type=${params.ad_type}&bot_limit=${params.bot_limit}&top_limit=${params.top_limit}&payment_method=${params.payment_method}&currency=${params.currency}`)
    commit('setOrders', data)
  },
  async createOrder({}, adForm) {
    return await this.$axios
      .post('/order/', adForm)
      .then(() => {
        this.$toast.showMessage({
          content: 'Ваше объявление успешно размещено!',
          green: true
        })
      })
      .catch(error => {
        this.$toast.showMessage({ content: error.response.data[0].message, red: true })
      })
  }
}
