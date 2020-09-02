import moment from "moment";

export default {
  methods: {
    timestampToUtc(timestamp) {
      return moment(timestamp)
        .utc()
        .format("DD.MM.YYYY HH:mm");
    },
    regularDate(timestamp) {
      return moment(timestamp)
        .utc()
        .format("DD.MM.YYYY");
    }
  }
};
