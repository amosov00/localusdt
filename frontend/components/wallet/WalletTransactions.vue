<template>
  <div>
    <h2 class="fw-500 mt-50">История транзакций</h2>
    <table class="table">
      <thead class="table__header">
        <tr class="table__row">
          <th class="table__head">Дата</th>
          <th class="table__head">Действие</th>
          <th class="table__head">Адрес</th>
          <th class="table__head">Сумма</th>
          <th class="table__head">Статус</th>
        </tr>
      </thead>
      <tbody class="table__body">
        <tr
          class="table__row"
          v-for="transaction in transactions"
          :key="transaction.date"
        >
          <td class="table__data">{{ regularDate(transaction.date) }}</td>
          <td class="table__data">{{ transactionEvent(transaction.event) }}</td>
          <td class="table__data">
            <span>
              {{ transaction.address }}
            </span>
            <a class="ml-15" :href="`https://etherscan.io/address/${transaction.address}`" target="_blank" rel="noopener noreferrer">
              <InlineSvg :src="require('~/assets/icons/redirect.svg')" />
            </a>
          </td>
          <td class="table__data">
            {{ commaSplitting(transaction.amount_usdt) }} USDT
          </td>
          <td
            class="table__data"
            :style="{ color: statusColor(transaction.status) }"
          >
            {{ transactionStatus(transaction.status) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import formatDate from '~/mixins/formatDate'
import formatCurrency from '~/mixins/formatCurrency'
import InlineSvg from 'vue-inline-svg'
export default {
  mixins: [formatDate, formatCurrency],
  components: {
    InlineSvg
  },
  computed: {
    ...mapGetters({
      transactions: 'wallet/transactions'
    })
  },
  methods: {
    transactionStatus(status) {
      switch (status) {
        case 1:
          return 'Обрабатывается'
          break
        case 2:
          return 'Отменена'
          break
        case 3:
          return 'Выполнено'
          break
        default:
          break
      }
    },
    transactionEvent(event) {
      switch (event) {
        case 1:
          return 'Пополнение USDT'
          break
        case 2:
          return 'Вывод USDT'
          break
        default:
          break
      }
    },
    statusColor(status) {
      switch (this.transactionStatus(status)) {
        case 'Выполнено':
          return '#48B190'
          break
        case 'Обрабатывается':
          return '#ED9F43'
          break
        case 'Отменена':
          return '#B31B11'
          break
      }
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
