export default function ({$axios, app}) {
    $axios.setToken(app.$cookies.get('token'), 'Bearer');

    $axios.onError(error => {
      switch (error.response.status) {
        case 401:
           if(error.response.data[0].message == 'User is not active') app.$authLogout()
          break
        default:
          break
      }
    })
}
