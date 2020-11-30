export default ({ app, store }, inject) => {
  inject('toast', {
    showMessage ({ content = '', color = '', red, green, timeout = 10000 }) {
      store.commit('toast/showMessage', { content, color, red, green, timeout })
    },
    closeToast() {
      store.commit('toast/closeToast')
    },
    openToast() {
      store.commit('toast/openToast')
    }
  })
}
