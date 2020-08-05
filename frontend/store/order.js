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
  async fetchOrders({ commit }, type = '') {
    const { data } = await this.$axios.get(`/order/?limit=100&${type ? `ad_type=${type}` : ''}`)
    commit('setOrders', data)
  },
  async fetchOrderById({ commit }, id) {
    const { data } = await this.$axios.get(`/order/${id}`)
    commit('setOrderById', data)
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
