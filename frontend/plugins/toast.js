export default ({ app, store }, inject) => {
  inject('toast', {
    showMessage ({ content = '', color = '', red, green }) {
      store.commit('toast/showMessage', { content, color, red, green })
    }
  })
}