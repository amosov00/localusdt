export const state = () => ({
  content: '',
  color: '',
  red: false,
  green: true,
  active: false,
})

export const mutations = {
  showMessage (state, payload) {
    state.content = payload.content
    state.color = payload.color
    state.red = payload.red
    state.green = payload.green
  },
  closeToast(s){s.active = false},
  openToast(s){s.active = true}
}
export const getters = {
  isActive(s) {
    return s.active
  }
}