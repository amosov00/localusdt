<template lang="pug">
  div
    table.table
      thead.table__header
        tr.table__row
          th.table__head Продавец
          th.table__head Способ оплаты
          th.table__head Лимит
          th.table__head Цена за токен
      tbody.table__body
        tr.table__row(v-for="order in tableData" :key="order._id")
          td.table__data {{order.username}}
            span.status.green--bg
            span.orders-count (10+)
          td.table__data 
            span {{paymentMethod(order.payment_method)}}
          td.table__data {{order.bot_limit}} - {{spaceSplitting(order.top_limit)}} ₽
          td.table__data {{commaSplitting(order.price)}} ₽
          td.table__data
            nuxt-link(:to="`/order/${order._id}`" v-if="order.type === 1")
              Button(rounded outlined green) Купить
            nuxt-link(:to="`/order/${order._id}`" v-else)
              Button(rounded outlined green) Продать
    div.pagination(v-if="pagination")
      div.pagination__controller
        span.pagination__arrow-button(@click="prevPage")
          InlineSvg(:src="require('~/assets/icons/arrow-left.svg')")
        span {{paginatedTableData}}
        span.pagination__arrow-button(@click="nextPage")
          InlineSvg(:src="require('~/assets/icons/arrow-right.svg')")
      div.pagination__quantity
</template>

<script>
import InlineSvg from 'vue-inline-svg'
import Button from '~/components/app/Button'
import formatCurreny from '~/mixins/formatCurrency'
import paymentMethod from '~/mixins/paymentMethod'
export default {
  props: {
    tableData: Array,
    pagination: {
      type: Boolean,
      default: false
    }
  },
  mixins: [formatCurreny, paymentMethod],
  components: {
    Button,
    InlineSvg
  },
  data() {
    return {
      currentPage: 1,
      contentPerPage: 25,
      tableContent: [],
      paginatedTableData: []
    }
  },
  watch: {
    currentPage: function(val) {
      let quantity = this.tableContent.slice(
        val * this.contentPerPage,
        this.contentPerPage
      )
    }
  },
  computed: {
    // paginatedTableData() {
    //   return this.tableContent.slice(
    //     this.currentPage * this.contentPerPage,
    //     this.contentPerPage
    //   )
    // }
  },
  methods: {
    prevPage() {
      this.currentPage -= 1
      console.log(this.currentPage, this.currentPage * this.contentPerPage)
    },
    nextPage() {
      this.currentPage += 1
      console.log(this.currentPage, this.currentPage * this.contentPerPage)
    }
  },
  created() {
    for (let i = 0; i < 300; i++) {
      this.tableContent.push(i)
    }
  }
}
</script>

<style lang="scss">
.table {
  max-width: 1230px;
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
    .table__row {
      line-height: 70px;

      &:nth-child(2n) {
        background-color: #fdfdfd;
      }

      &:hover {
        background-color: #fdfdfd;
      }
    }
  }

  &__data {
    text-align: left;
    padding-left: 30px;

    .status {
      display: inline-block;
      height: 10px;
      width: 10px;
      border-radius: 50%;
      margin-left: 6px;
    }

    .orders-count {
      display: inline-block;
      margin-left: 15px;
      color: $grey-dark;
    }

    &:not(:last-child) {
      border-right: 1px solid $grey;
    }

    &:nth-child(4) {
      font-weight: 500;
    }
  }
}

.pagination {
  width: 100%;
  height: 20px;
  display: flex;
  justify-content: center;

  &__controller {
    display: inline-block;
    max-width: 350px;
    width: 100%;
    height: 20px;
    display: flex;
    justify-content: space-between;
  }

  &__arrow-button {
    cursor: pointer;
  }

  &__quantity {
    justify-self: end;
    display: inline-block;
    width: 100px;
    height: 20px;
  }
}
</style>
