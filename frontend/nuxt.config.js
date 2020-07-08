export default {
  mode: 'spa',

  head: {
    title: 'LocalUSDT',
    meta: [
      {charset: 'utf-8'},
      {name: 'viewport', content: 'width=device-width, initial-scale=1'},
      {hid: 'description', name: 'description', content: ''}
    ],
    link: [
      {rel: "icon", type: "image/x-icon", href: "/favicon.ico"},
    ]
  },

  loading: {color: '#0495FB'},

  css: [
    {src: '~/assets/scss/main.scss', lang: 'scss'},
    {src: '~/assets/scss/transition.scss', lang: 'scss'},
    {src: '@fortawesome/fontawesome-free/css/all.css', lang: 'css'},
  ],

  plugins: [
    '~/plugins/auth.js',
    '~/plugins/axios.js',
  ],
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/dotenv',
    '@nuxtjs/sentry',
    ['nuxt-buefy', {css: false}],
    'cookie-universal-nuxt',
  ],
  buildModules: [
    '@nuxtjs/dotenv'
  ],
  dotenv: !process.env.ENV ? {
    filename: '.env.local',
  } : {},
  sentry: {
    initialize: true,
    config: {
      environment: process.env.ENV,
    },
  },
  build: {
    extend(config, ctx) {
    }
  }
}
