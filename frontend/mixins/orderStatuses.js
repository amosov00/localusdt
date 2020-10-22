export default {
  methods: {
    // 1 - ACTIVE, 2 - NOT_ACTIVE, 3 - DELETED
    orderStatus(status) {
      switch (status) {
        case 1:
          return this.$t('status.active')
          break
        case 2:
          return this.$t('status.notActive')
          break
        case 3:
          return this.$t('status.deleted')
          break
      }
    },
    orderStatusColor(status) {
      switch (status) {
        case 1:
          return '#48B190'
          break
        case 2:
          return '#ED9F43'
          break
        case 3:
          return '#B31B11'
          break
      }
    }
  }
}
