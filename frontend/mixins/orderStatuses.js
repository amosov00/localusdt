export default {
  methods: {
    // 1 - ACTIVE, 2 - NOT_ACTIVE, 3 - DELETED
    orderStatus(status) {
      switch (status) {
        case 1:
          return 'Активно'
          break
        case 2:
          return 'Не активно'
          break
        case 3:
          return 'Удален'
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
