export const state = () => ({
  transactions: []
})

export const getters = {
  transactions: s => s.transactions
}

export const mutations = {
  setTransactions: (state, payload) => {
    state.transactions = payload
  }
}

export const actions = {
  async withdraw({}, payload) {
    return this.$axios.post('/account/withdraw/', payload)
      .then((res) => {
        console.log(res);
        return true
      })
      .catch(() => false)
  },

  async fetchTransactions({ commit }) {
    const { data } = await this.$axios.get('/account/transactions/')
    commit('setTransactions', data)
  }
}
