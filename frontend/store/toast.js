export const state = () => ({
  content: '',
  color: '',
  red: false,
  green: true,
  active: false,
})

export const mutations = {
  showMessage (state, { content, color, red, green, timeout }) {
    state.content = content
    state.color = color
    state.red = red
    state.green = green
    state.timeout = timeout
  },

  closeToast(s) {
    s.active = false
  },

  openToast(s){
    s.active = true
  }
}
export const getters = {
  isActive(s) {
    return s.active
  }
}
