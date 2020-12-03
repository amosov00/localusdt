export default {
  methods: {
    paymentMethod(method) {
      switch (method) {
        case 1:
          return `${this.$t('main.bankTransfer')} ${this.$t('main.sberbank')}`
        case 2:
          return `${this.$t('main.bankTransfer')} ${this.$t('main.tinkof')}`
        case 3:
          return `${this.$t('main.bankTransfer')} ${this.$t('main.alfa')}`
        case 4:
          return `${this.$t('main.otherWay')}}`
        case 5:
          return `${this.$t('main.all')}`
        case 6:
          return `${this.$t('main.bankTransfer')} ${this.$t('main.cardToCard')}`
        case 7:
          return `${this.$t('main.qiwi')}`
        case 8:
          return `${this.$t('main.yandex')}`
        case 9:
          return `${this.$t('main.payeer')}`
        case 10:
          return `${this.$t('main.payPal')}`
        case 11:
          return `${this.$t('main.cash')}`
        case 11:
          return `${this.$t('main.webMoney')}`
        default:
          break;
      }
    }
  },
}