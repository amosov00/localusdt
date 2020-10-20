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
        default:
          break;
      }
    }
  },
}