export default {
  methods: {
    invoiceStatus(status) {
      switch (status) {
        case 'waiting_for_payment':
          return 'Ожидание подтверждения платежа покупателем'
          break
        case 'approved':
          return 'Подтверждено'
          break
        case 'waiting_for_tokens':
          return 'Ожидание отправки токенов'
          break
        case 'completed':
          return 'Завершен'
          break
        case 'cancelled':
          return 'Отменен'
          break
      }
    },
    invoiceStatusShort(status) {
      switch (status) {
        case 'waiting_for_payment':
          return 'В процессе'
          break
        case 'approved':
          return 'Завершен'
          break
        case 'waiting_for_tokens':
          return 'В процессе'
          break
        case 'completed':
          return 'Завершен'
          break
        case 'cancelled':
          return 'Отменена'
          break
      }
    },
    statusColor(status) {
      switch (this.invoiceStatusShort(status)) {
        case 'Завершен':
          return '#48B190'
          break
        case 'В процессе':
          return '#ED9F43'
          break
        case 'Отменена':
          return '#B31B11'
          break
      }
    }
  }
}
