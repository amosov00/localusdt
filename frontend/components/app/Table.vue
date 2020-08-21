<template lang="pug">
  div
    table.table
      thead.table__header
        tr.table__row
          th.table__head Продавец
          th.table__head Способ оплаты
          th.table__head Лимит
          th.table__head Количество
          th.table__head Цена за токен
      tbody.table__body
        tr.table__row(v-for="order in paginatedTableData" :key="order._id")
          td.table__data {{order.username}}
            span.status.green--bg
            span.orders-count (10+)
          td.table__data 
            span {{paymentMethod(order.payment_method)}}
          td.table__data {{spaceSplitting(order.bot_limit)}} - {{spaceSplitting(order.top_limit)}} ₽
          td.table__data
            span {{spaceSplitting(order.amount_usdt)}} USDT
          td.table__data {{commaSplitting(order.price)}} ₽
          td.table__data
            nuxt-link(:to="`/order/${order._id}`" v-if="order.type === 1")
              Button(rounded outlined green) {{buttonName}}
            nuxt-link(:to="`/order/${order._id}`" v-else)
              Button(rounded outlined green) {{buttonName}}
    div.pagination(v-if="pagination")
      div.pagination__controller
        button.pagination__arrow-button(@click="prevPage")
          InlineSvg.pagination__arrow-icon(:src="require('~/assets/icons/arrow-left.svg')")
        p
          button.pagination__page-button(v-for="page in pagesCount" :key="page" @click="goToPage(page)" :class="{'orange': currentPage === page}" ) {{page}}
        button.pagination__arrow-button(@click="nextPage")
          InlineSvg.pagination__arrow-icon(:src="require('~/assets/icons/arrow-right.svg')")
      div.pagination__quantity
        button.pagination__quantity-button(:class="{'black': contentPerPage === 15}" @click="contentPerPage = 15" ) 15
        button.pagination__quantity-button(:class="{'black': contentPerPage === 25}" @click="contentPerPage = 25" ) 25
        button.pagination__quantity-button(:class="{'black': contentPerPage === 50}" @click="contentPerPage = 50" ) 50
        button.pagination__quantity-button(:class="{'black': contentPerPage === 100}" @click="contentPerPage = 100" ) 100
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
    },
    buttonName: String
  },
  mixins: [formatCurreny, paymentMethod],
  components: {
    Button,
    InlineSvg
  },
  data() {
    return {
      currentPage: 1,
      contentPerPage: 15
    }
  },
  computed: {
    whichTable() {
      switch (this.pagination) {
        case true:
          return 'paginatedTableData'
          break
        case false:
          return 'tableData'
          break

        default:
          break
      }
    },
    paginatedTableData() {
      return this.tableData.slice(
        this.currentPage * this.contentPerPage - this.contentPerPage,
        this.currentPage * this.contentPerPage
      )
    },
    pagesCount() {
      return Math.ceil(this.tableData.length / this.contentPerPage)
    }
  },
  methods: {
    prevPage() {
      if (this.currentPage <= 1) {
        return
      }
      this.currentPage -= 1
    },
    nextPage() {
      if (this.paginatedTableData.length / this.contentPerPage < 1) {
        return
      }
      this.currentPage += 1
    },
    goToPage(page) {
      this.currentPage = page
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
      opacity: 0.3;
      font-weight: 500;
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
  max-width: 1230px;
  width: 100%;
  height: 20px;
  display: flex;
  justify-content: center;
  position: relative;

  &__controller {
    display: inline-block;
    max-width: 350px;
    width: 100%;
    height: 20px;
    display: flex;
    justify-content: space-between;
  }

  &__arrow-button {
    @include reset-button;
  }

  &__page-button {
    color: $grey-dark;
    @include reset-button;

    &:not(:last-child) {
      margin-right: 30px;
    }
  }

  &__quantity {
    position: absolute;
    top: 0;
    right: 0;
    display: inline-block;
    width: 115px;
    height: 20px;

      &:not(:last-child) {
        margin-right: 5px;
      }
  }

  &__quantity-button {
    @include reset-button;
    transition: $interaction-transition;
    color: $grey-dark;

    &:hover {
      color: $black;
    }

    &:not(:last-child) {
      margin-right: 10px;
    }
  }
}
</style>
