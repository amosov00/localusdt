export const state = () => ({
  locales: [
    {
      code: 'ru',
      name: 'RU',
      id: 1
    },
    {
      code: 'en',
      name: 'EN',
      id: 2
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
  },
  GET_LOCALE_ID(state) {
    return state.locales.find(el => el.code === state.locale).id
  },

  GET_LOCALE_ID_BY_CODE: (state) => (code) => {
    return state.locales.find(locale => locale.code === code).id
}
}
