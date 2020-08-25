export const state = () => ({
  orders: [],
  orderById: null
})

export const getters = {
  orders: s => s.orders,
  orderById: s => s.orderById,
  buyOrders: s => s.orders.filter(order => order.type === 1),
  sellOrders: s =>
    s.orders
      .filter(order => order.type === 2)
      .sort((a, b) => b.price - a.price),
  buyOrdersWithLimit: s => limit => {
    return s.orders.filter(order => order.type === 1).slice(0, limit)
  },
  sellOrdersWithLimit: s => limit => {
    return s.orders
      .filter(order => order.type === 2)
      .sort((a, b) => b.price - a.price)
      .slice(0, limit)
  }
}

export const mutations = {
  setOrders: (state, payload) => (state.orders = payload),
  setOrderById: (state, payload) => (state.orderById = payload)
}

export const actions = {
  async fetchOrders({ commit }, query) {
    const { data } = await this.$axios.get(
      `/order/?limit=${query.limit}&${
        query.type ? `order_type=${query.type}` : ''
      }&${query.currency ? `currency=${query.currency}` : ''}&${
        query.payment_method ? `payment_method=${query.payment_method}` : ''
      }&${query.price_bot ? `price_bot=${query.price_bot}` : ''}&${
        query.price_top ? `price_top=${query.price_top}` : ''
      }&${query.sort ? `sort=${query.sort}` : ''}`
    )
    commit('setOrders', data)
  },
  async fetchOrderById({ commit }, id) {
    const { data } = await this.$axios.get(`/order/${id}`)
    commit('setOrderById', data)
  },
  async searchOrders({ commit }, params) {
    const { data } = await this.$axios.get(
      `/order/?order_type=${params.ad_type}&bot_limit=${params.bot_limit}&top_limit=${params.top_limit}&payment_method=${params.payment_method}&currency=${params.currency}`
    )
    commit('setOrders', data)
  },


  async createOrder({}, adForm) {
    return await this.$axios
      .post('/order/', adForm)
      .then(() => {
        return true
      })
      .catch(error => {
        switch (error.response.data[0].message) {
          case 'Can\'t get currency rate.':
            this.$toast.showMessage({
              content: 'Невозможно получить актуальный курс USDT/RUB',
              red: true
            })
            break;
          case 'Not enough USDT':
            this.$toast.showMessage({
              content: 'Недостаточно USDT на аккаунте',
              red: true
            })
            break;
          default:
            this.$toast.showMessage({
              content: error.response.data[0].message,
              red: true
            })
        }
        return false
      })
  }
}
