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
  async fetchTransactions({ commit }) {
    const { data } = await this.$axios.get('/account/transactions/')
    commit('setTransactions', data)
    console.log(data)
  }
}
