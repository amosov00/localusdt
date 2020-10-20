export const state = () => ({
  locales: [
    {
      code: 'ru',
      name: 'RU'
    },
    {
      code: 'en',
      name: 'EN'
    }
  ],
  locale: 'en'
})

export const mutations = {
  SET_LANG(state, locale) {
    if (state.locales.find(el => el.code === locale)) {
      state.locale = locale
    }
  }
}

export const getters = {
  GET_LOCALE(state) {
    return state.locale
  }
}
