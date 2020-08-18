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
          span.status.green--bg
          span.orders-count (10+)
        td.table__data {{commaSplitting(invoice.amount_usdt)}} USDT 
          span.opacity-50.fw-400 за {{commaSplitting(invoice.amount_rub)}} ₽
        td.table__data(:style="{ color: statusColor(invoice.status) }")
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
    },
  },
  methods: {
    statusColor(status) {
      switch (this.invoiceStatusShort(status)) {
        case 'Завершен':
          return '#48B190'
          break;
        case 'В процессе':
          return '#ED9F43'
          break;
        case 'Отменена':
          return '#B31B11'
          break;
      }
    }
  }
}
</script>

