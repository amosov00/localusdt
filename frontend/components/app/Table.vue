<template lang="pug">
  table.table
    thead.table__header
      tr.table__row
        th.table__head Продавец
        th.table__head Способ оплаты
        th.table__head Лимит
        th.table__head Цена за токен
    tbody.table__body
      tr.table__row(v-for="ad in tableData" :key="ad._id")
        td.table__data {{ad.username}}
          span.status.green--bg
        td.table__data Банковский перевод: {{ad.bank_title}}
        td.table__data {{ad.bot_limit}} - {{spaceSplitting(ad.top_limit)}} ₽
        td.table__data {{commaSplitting(ad.price)}} ₽
        td.table__data
          nuxt-link(:to="`/ad/${ad._id}`" v-if="isBuy")
            Button(rounded outlined green) Купить
          nuxt-link(:to="`/ad/${ad._id}`" v-else)
            Button(rounded outlined green) Продать
</template>

<script>
import Button from '~/components/app/Button'
import formatCurreny from '~/mixins/formatCurrency'
export default {
  props: {
    tableData: Array
  },
  mixins: [formatCurreny],
  components: {
    Button
  },
  data() {
    return {
    }
  },
  computed: {
    isBuy() {
      if(this.tableData[0].type === 1) {
        return false
      } else {
        return true
      }
    }
  },
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
}
</style>
