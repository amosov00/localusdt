export default {
  methods: {
    paymentMethod(method) {
      switch (method) {
        case 1:
          return 'Банковский перевод: Сбербанк'
        case 2:
          return 'Банковский перевод: Тинькофф'
        case 3:
          return 'Банковский перевод: Альфа Банк'
        case 4:
          return 'Иной способ'
        default:
          break;
      }
    }
  },
}