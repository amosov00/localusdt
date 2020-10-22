import moment from 'moment'

export default {
  methods: {
    timestampToUtc(timestamp) {
      return moment(timestamp)
        .utc()
        .format('DD.MM.YYYY HH:mm')
    },
    regularDate(timestamp) {
      return moment(timestamp)
        .utc()
        .format('DD.MM.YYYY')
    },
    formatDate(time) {
      const offset = moment().utcOffset()
      return moment(time).add(offset, 'minutes').format('DD.MM.YYYY HH:mm')
    }
  }
}
