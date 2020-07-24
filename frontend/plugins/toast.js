export default ({ app, store }, inject) => {
  inject('toast', {
    showMessage ({ content = '', color = '' }) {
      store.commit('toast/showMessage', { content, color })
    }
  })
}