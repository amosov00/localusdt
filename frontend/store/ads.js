export const state = () => ({
  ads: []
})

export const getters = {
  ads: s => s.ads
}

export const mutations = {
  setAds: (state, payload) => (state.ads = payload)
}

export const actions = {
  async fetchAds({ commit }, limit = 10) {
    const { data } = await this.$axios.get('/ads', {
      params: {
        limit
      }
    })
    console.log(data)
  }
}
