export const state = () => ({
  ads: [],
  adById: null
})

export const getters = {
  ads: s => s.ads,
  adById: s => s.adById,
  buyAds: s => s.ads.filter(ad => ad.type === 1),
  sellAds: s => s.ads.filter(ad => ad.type === 2)
}

export const mutations = {
  setAds: (state, payload) => (state.ads = payload),
  setAdById: (state, payload) => (state.adById = payload)
}

export const actions = {
  async fetchAds({ commit }, type = '') {
    const { data } = await this.$axios.get(`/adv/?limit=100&${type ? `ad_type=${type}` : ''}`)
    commit('setAds', data)
  },
  async fetchAdById({ commit }, id) {
    const { data } = await this.$axios.get(`/adv/${id}`)
    commit('setAdById', data)
  },
  async createAd({}, adForm) {
    return await this.$axios
      .post('/adv/', adForm)
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
