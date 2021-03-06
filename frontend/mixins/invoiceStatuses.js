export default {
  methods: {
    invoiceStatus(status) {
      switch (status) {
        case 'waiting_for_payment':
          return this.$t('status.waiting_for_payment')
          break
        case 'approved':
          return this.$t('status.approved')
          break
        case 'waiting_for_tokens':
          return this.$t('status.waiting_for_tokens')
          break
        case 'completed':
          return this.$t('status.completed')
          break
        case 'cancelled':
          return this.$t('status.cancelled')
          break
        case 'frozen':
          return this.$t('status.frozen')
          break
      }
    },
    invoiceStatusShort(status) {
      switch (status) {
        case 'waiting_for_payment':
          return this.$t('status.small_waiting_for_payment')
          break
        case 'approved':
          return this.$t('status.small_approved')
          break
        case 'waiting_for_tokens':
          return this.$t('status.small_waiting_for_tokens')
          break
        case 'completed':
          return this.$t('status.small_completed')
          break
        case 'cancelled':
          return this.$t('status.cancelled')
          break
        case 'frozen':
          return this.$t('status.frozen')
          break
      }
    },
    invoiceStatusNumber(status) {
      switch (status) {
        case 1:
          return 'IN_PROGRESS'
          break
        case 2:
          return 'CANCELLED'
          break
        case 3:
          return 'DONE'
          break
      }
    },
    statusColor(status) {
      switch (status) {
        case 'approved':
        case 'completed':
          return '#48B190'
          break
        case 'waiting_for_payment':
        case 'waiting_for_tokens':
          return '#ED9F43'
          break
        case 'cancelled':
          return '#B31B11'
        case 'frozen':
          return '#EFA543'
          break
      }
    }
  }
}
