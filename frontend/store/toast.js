export const state = () => ({
  content: '',
  color: '',
  red: false,
  green: true
})

export const mutations = {
  showMessage (state, payload) {
    state.content = payload.content
    state.color = payload.color
    state.red = payload.red
    state.green = payload.green
  }
}