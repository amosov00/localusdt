import _ from 'lodash'

let cookieOpts = {
  path: '/',
  maxAge: 60 * 60 * 24 * 7,
}

// if (process.env.NODE_ENV === 'production') {
//   const additional = {
//     sameSite: 'none',
//     secure: true
//   }

//   cookieOpts = { ...additional }
// }

export const state = () => ({
  user: null,
  currencyPrice: null,
  currencyFullData: null,
})

export const getters = {
  user: s => s.user,
  currencyPrice: s => s.currencyPrice,
  currencyFullData: s => s.currencyFullData
}

export const mutations = {
  setUser: (state, user) => (state.user = user),
  setBalance: (state, balance) => (state.user.balance_usdt = balance),
  deleteUser: state => (state.user = false),
  setCurrencyPrice: (state, payload) => (state.currencyPrice = payload.current_rate),
  currencyFullData(state, payload){
    state.currencyFullData = payload
  }

}

export const actions = {
  async signUp({ commit }, data) {
    if (!data) return false
    return await this.$axios
      .post('/account/signup/', data)
      .then(resp => {
        this.$axios.setToken(resp.data.token, 'Bearer')
        this.$cookies.set('token', resp.data.token, cookieOpts)
        commit('setUser', resp.data.user)
        this.$toast.showMessage({
          content: $nuxt.$t('store.register'),
          green: true,
          timeout: 60000,
        })
        return this.$router.push('/')
      })
      .catch(error => {
        switch (error.response.data[0].message) {
          case 'Пользователь с таким email уже существует':
            this.$toast.showMessage({
              content: $nuxt.$t('store.signUpEmailError'),
              red: true
            })
            break
          default:
            this.$toast.showMessage({
            content: $nuxt.$t('store.signUpError'),
            red: true
          })
        }
      })
  },
  async logIn({ commit }, { email, userName, password, passwordRepeat }) {
    return await this.$axios
      .post('/account/login/', {
        email,
        password,
        username: userName,
        repeat_password: passwordRepeat
      })
      .then(({ data }) => {
        const { token, user } = data;
        
        this.$axios.setToken(token, 'Bearer')
        this.$cookies.set('token', token, cookieOpts)

        commit('setUser', user)
        this.$toast.showMessage({
          content: $nuxt.$t('store.login'),
          green: true
        })
        this.$router.push({ path: '/' })
      })
      .catch(error => {
        if(error.response.data[0].message == 'activate email or you are blocked'){
          this.$toast.showMessage({
            content: $nuxt.$t('store.signInError'),
            red: true
          })
          throw new Error("Ошибка!")
        }
        this.$toast.showMessage({
          content: $nuxt.$t('store.signInError'),
          red: true
        })
      })
  },
  logOut({ commit }) {
    commit('deleteUser')
    this.$axios.setToken(null)
    this.$cookies.remove('token')
    this.$router.push('/')
  },
  async fetchUser({ commit }) {
    const { data } = await this.$axios.get('account/user/')
    commit('setUser', data)
  },
  async fetchBalance({ commit }) {
    const { data } = await this.$axios.get('account/user/', { progress: false })
    commit('setBalance', data.balance_usdt)
  },
  async changeProfile({}, data) {
    console.log('/account/user/');
    return await this.$axios
      .put('/account/user/', data)
      .then(_ => {
        return true
      })
      .catch(err => {
        return false
      })
  },
  async changePassword({}, data) {
    return await this.$axios
      .post('/account/change_password/', data)
      .then(_ => {
        this.$toast.showMessage(
          {
            content: $nuxt.$t('store.passChange'),
            green: true
          })
        this.$router.push('/profile')
      })
      .catch(error => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.changePassError'),
          red: true
        })
      })
  },
  async activateAccount({}, data) {
    return await this.$axios
      .post('/account/verify/', data)
      .then(resp => {
        return resp.data
      })
      .catch(() => {
        return false
      })
  },
  async startRecover({}, data) {
    return await this.$axios
      .post('/account/recover/', data)
      .then(_ => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.checkEmail'),
          green: true
        })
        this.$router.push('/')
        return true
      })
      .catch(error => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.recoverPassError'),
          red: true
        })
      })
  },
  async finishRecover({}, data) {
    return await this.$axios
      .put('/account/recover/', data)
      .then(_ => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.passRecover'),
          green: true
        })
        this.$router.push('/login')
        return true
      })
      .catch(error => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.recoverPassError'),
          red: true
        })
      })
  },
  async changeCondition({ dispatch }, condition) {
    console.log('/account/user/');
    await this.$axios
      .put('/account/user/', {
        about_me: condition
      })
      .then(() => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.infoChange'),
          green: true
        })
        dispatch('fetchUser')
      })
      .catch(error => {
        this.$toast.showMessage({
          content: $nuxt.$t('store.infoChangeError'),
          red: true
        })
      })
  },
  async fetchCurrencyPrice({ commit }, payload = 1) {
    let  result = await this.$axios.get(`/currency/?currency=${payload}`)
    console.log(1);
      commit('setCurrencyPrice', result.data)
      commit('currencyFullData', result.data)
  },
  async fetchReferralInfo({}) {
    return this.$axios.get('/account/referral_info/')
      .then(res => res.data)
      .catch((e) => {
        console.log(e)
        this.$toast.showMessage({
          content: $nuxt.$t('store.refError'),
          red: true
        })
      })
  },
}
