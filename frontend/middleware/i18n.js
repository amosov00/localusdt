export default function({ app, store}) {
  let locale = localStorage.getItem('locale')
  locale = locale ? locale : 'en'
  store.commit('i18n/SET_LANG', locale)
  app.i18n.locale = locale
}