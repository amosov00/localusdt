export const state = () => ({
  orders: [],
  orderById: null,
  ordersByUser: []
})

export const getters = {
  orders: s => s.orders,
  orderById: s => s.orderById,
  ordersByUser: s => s.ordersByUser,
  buyOrders: s => s.orders.filter(order => order.type === 1),
  sellOrders: s =>
    s.orders
      .filter(order => order.type === 2)
      .sort((a, b) => b.price - a.price),
  buyOrdersWithLimit: s => limit => {
    return s.orders.filter(order => order.currency === 1).slice(0, limit)
  },
  sellOrdersWithLimit: s => limit => {
    return s.orders
      .filter(order => order.type === 2 && order.currency == 1)
      .sort((a, b) => b.price - a.price)
      .slice(0, limit)
  }
}

export const mutations = {
  setOrders: (state, payload) => (state.orders = payload),
  setOrderById: (state, payload) => (state.orderById = payload),
  setOrdersByUser: (state, payload) => (state.ordersByUser = payload)
}

export const actions = {
  async fetchOrders({ commit }, query) {
    let data = await this.$axios.get(
      `/order/?limit=${query.limit}&${
        query.type ? `order_type=${query.type}` : ''
      }&${query.currency ? `currency=${query.currency}` : ''}&${
        query.payment_method ? `payment_method=${query.payment_method}` : ''
      }&${query.price_bot ? `price_bot=${query.price_bot}` : ''}&${
        query.price_top ? `price_top=${query.price_top}` : ''
      }&${query.sort ? `sort=${query.sort}` : ''}`
    )
    commit('setOrders', data.data)
  },
  async fetchOrderById({ commit }, id) {
    const { data } = await this.$axios.get(`/order/${id}`)
    commit('setOrderById', data)
  },
  async fetchOrdersByUser({ commit }) {
    const { data } = await this.$axios.get(`/order/user/`)
    commit('setOrdersByUser', data)
  },
  async searchOrders({ commit }, params) {
    console.log(params.currency);
    let url = `/order/?order_type=${params.ad_type}&bot_limit=${params.bot_limit}&top_limit=${params.top_limit}${params.payment_method == 5 ? '' : `&payment_method=${params.payment_method}`}&currency=${params.currency}`
    console.log('url', url);
    const { data } = await this.$axios.get(url)
    console.log('data', data);
    data.forEach(e => {
      e.setCurrency = params.currency
    });
    commit('setOrders', data)
  },

  async setOrderStatus({}, payload) {
    return await this.$axios
      .put(`/order/${payload.id}/${payload.endpoint}/`)
      .then(() => {
        this.$toast.showMessage({
          content: `${$nuxt.$t('store.statusChange')} ${payload.endpoint.toUpperCase()}`,
          green: true
        })
        return true
      })
      .catch(() => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.statusChangeError'),
          red: true
        })
        return false
      })
  },

  async updateOrder({}, payload) {
    return await this.$axios
      .put(`/order/${payload.id}/update/`, payload.data)
      .then(() => true)
      .catch(() => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.orderSaveError'),
          red: true
        })
        return false
      })
  },

  async removeOrder({}, orderId) {
    return await this.$axios
      .put(`/order/${orderId}/delete/`)
      .then(() => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.orderDelete'),
          green: true
        })
        return true
      })
      .catch(() => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.orderDeleteError'),
          red: true
        })
        return false
      })
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
              content: $nuxt.$t('store.courseError'),
              red: true
            })
            break;
          case 'Not enough USDT':
            this.$toast.showMessage({
              content: $nuxt.$t('store.statusError4'),
              red: true
            })
            break;
          default:
            this.$toast.showMessage({
              content: $nuxt.$t('store.orderCreateError'),
              red: true
            })
        }
        return false
      })
  }
}
