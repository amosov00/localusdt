export default {
  methods: {
    spaceSplitting(value) {
      return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
    },
    commaSplitting(value) {
      return value.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    }
  }
}
