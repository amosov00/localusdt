import _ from 'lodash'

export const state = () => ({
  user: null
})

export const getters = {
  user: s => s.user
}

export const mutations = {
  setUser: (state, user) => (state.user = user),
  deleteUser: state => (state.user = false)
}

export const actions = {
  async signUp({ commit }, data) {
    if (!data) return false
    return await this.$axios
      .post('/account/signup/', data)
      .then(resp => {
        this.$axios.setToken(resp.data.token, 'Bearer')
        this.$cookies.set('token', resp.data.token, {
          path: '/',
          maxAge: 60 * 60 * 24 * 7
        })
        commit('setUser', resp.data.user)
        this.$toast.showMessage({ content: 'Вы успешно зарегистрировались, проверьте почту для активации аккаунта', green: true })
        return this.$router.push('/')
      })
      .catch((error) => {
        this.$toast.showMessage({ content: error.response.data.detail[0].msg, red: true })
      })
  },
  async logIn({ commit }, data) {
    return await this.$axios
      .post('/account/login/', {
        email: data.email,
        username: data.userName,
        password: data.password,
        repeat_password: data.passwordRepeat
      })
      .then(resp => {
        this.$axios.setToken(resp.data.token, 'Bearer')
        this.$cookies.set('token', resp.data.token, {
          path: '/',
          maxAge: 60 * 60 * 24 * 7
        })
        commit('setUser', resp.data.user)
        this.$toast.showMessage({ content: 'Успешный вход в систему!', green: true })
        this.$router.push({ path: '/' })
      })
      .catch(error => {
        this.$toast.showMessage({ content: error.response.data[0].message, red: true })
      })
  },
  logOut({ commit }) {
    commit('deleteUser')
    this.$axios.setToken(null)
    this.$cookies.remove('token')
    this.$router.push('/')
  },
  async changeProfile({}, data) {
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
        this.$toast.showMessage({ content: 'Пароль изменен!', green: true })
        this.$router.push('/profile')
      })
      .catch(error => {
        this.$toast.showMessage({ content: error.response.data[0].message, red: true })
      })
  },
  async activateAccount({}, data) {
    return await this.$axios
      .post('/account/verify/', data)
      .then(resp => {
        return resp.data;
      })
      .catch(() => {
        return false
      })
  },
  async startRecover({}, data) {
    return await this.$axios
      .post('/account/recover/', data)
      .then(_ => {
        this.$toast.showMessage({ content: ' Проверьте свою почту!', green: true })
        this.$router.push('/')
        return true
      })
      .catch(error => {
        this.$toast.showMessage({ content: error.response.data[0].message, red: true })
      })
  },
  async finishRecover({}, data) {
    return await this.$axios
      .put('/account/recover/', data)
      .then(_ => {
        this.$toast.showMessage({ content: ' Пароль успешно восстановлен!', green: true })
        this.$router.push('/login')
        return true
      })
      .catch(error => {
        this.$toast.showMessage({ content: error.response.data[0].message, red: true })
      })
  }
}
