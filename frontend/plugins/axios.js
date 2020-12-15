export default function ({$axios, app}) {
    $axios.setToken(app.$cookies.get('token'), 'Bearer');

    $axios.onError(error => {
      switch (error.response.status) {
        case 401:
            app.$authLogout()
          break
        default:
          break
      }
    })
}
