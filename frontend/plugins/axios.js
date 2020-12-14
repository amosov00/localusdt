export default function ({$axios, app}) {
    $axios.setToken(app.$cookies.get('token'), 'Bearer');

    $axios.onError(error => {
      switch (error.response.status) {
        case 401:
          setTimeout(() => {
            app.$authLogout()
          }, 10000);
          break
        default:
          break
      }
    })
}
