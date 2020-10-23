export default function ({$axios, app}) {

    if(process.server) {
      console.log(process.env.API_URL_BROWSER)

    }

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
