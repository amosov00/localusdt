<template lang="pug">
  table.table
    thead.table__header
      tr.table__row
        th.table__head Дата, время
        th.table__head Вид сделки
        th.table__head Покупатель/продавец
        th.table__head Сумма
        th.table__head Статус
    tbody.table__body
      tr.table__row(v-for="invoice in tableData" :key="invoice._id")
        td.table__data {{timestampToUtc(invoice.created_at)}}
        td.table__data(v-if="invoice.ads_type === 1") Покупка USDT
        td.table__data(v-else-if="invoice.ads_type === 2") Продажа USDT
        td.table__data {{invoice.seller_username}}
        td.table__data {{commaSplitting(invoice.amount_usdt)}} USDT 
          span.opacity-50 за {{commaSplitting(invoice.amount_rub)}} ₽
        td.table__data.orange
          nuxt-link.table__link( :to="`/invoice/${invoice._id}`")  {{invoiceStatusShort(invoice.status)}}
</template>

<script>
import Button from '~/components/app/Button'
import formatCurreny from '~/mixins/formatCurrency'
import formatDate from '~/mixins/formatDate'
import invoiceStatuses from '~/mixins/invoiceStatuses'
export default {
  props: {
    tableData: Array
  },
  mixins: [formatCurreny, formatDate, invoiceStatuses],
  components: {
    Button
  },
  data() {
    return {}
  },
  computed: {
    isBuy() {
      if (this.tableData[0].type === 1) {
        return false
      } else {
        return true
      }
    }
  },
  methods: {
  }
}
</script>

<style lang="scss">
.table {
  max-width: 1170px;
  width: 100%;
  border-collapse: collapse;
  margin: 25px 0;
  text-align: center;
  &__header {
    .table__row {
      color: #000;
      opacity: 0.4;
      text-transform: uppercase;
      text-align: center;
    }
  }

  &__head {
    padding: 20px;
    font-weight: 500;
  }

  &__body {
    border: 1px solid $grey;
    border-radius: 3px;

    .table__row {
      line-height: 70px;
      &:nth-child(2n) {
        background-color: rgba(72, 177, 144, 0.07);
      }

      &:hover {
        background-color: rgba(72, 177, 144, 0.07);
      }
    }
  }

  &__data {
    // padding: 25px;
    border-right: 1px solid $grey;
    position: relative;
  }

  &__link {
    color: $orange !important;
  }
}
</style>
