export default {
  mode: 'spa',

  head: {
    title: 'LocalUSDT',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;600;700&display=swap'
      },
      {
        rel: 'stylesheet',
        href:
          'https://fonts.googleapis.com/css2?family=Montserrat:wght@100;300;400;500;600;700&display=swap'
      }
    ]
  },

  loading: { color: '#48B190' },

  css: ['~/assets/scss/global.scss'],

  env: {
    API_WS_URL: process.env.API_WS_URL
  },

  plugins: [
    '~/plugins/perfect-scrollbar',
    '~/plugins/auth.js',
    '~/plugins/axios.js',
    '~/plugins/toast.js',
    '~/plugins/vee-validate.js',
    '~/plugins/vue-clipboard.js',
    '~/plugins/vue-notification.js',
    '~/plugins/i18n.js',
    {src:'~/plugins/vue-socket.client.js',  mode: 'client', ssr: false }
  ],
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/dotenv',
    '@nuxtjs/sentry',
    'cookie-universal-nuxt',
    '@nuxtjs/style-resources'
  ],
  router: {
    middleware: ['checkRef', 'i18n']
  },
  styleResources: {
    scss: ['~/assets/scss/variables.scss', '~/assets/scss/mixins.scss']
  },
  buildModules: ['@nuxtjs/dotenv'],
  dotenv: 'local'
    ? {
        filename: '.env.local'
      }
    : {},
  sentry: {
    initialize: true,
    config: {
      environment: 'local'
    }
  },
  build: {
    vendor: ['vue-i18n'],
    extend(config, ctx) {
      config.module.rules.push({
        test: /\.(ogg|mp3|wav|mpe?g)$/i,
        loader: 'file-loader',
        options: {
          name: '[path][name].[ext]'
        }
      })
    }
  }
}
