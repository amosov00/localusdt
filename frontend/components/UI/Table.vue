<template lang="pug">
  table.table
    thead.table__header
      tr.table__row
        th.table__head Продавец
        th.table__head Способ оплаты
        th.table__head Лимит
        th.table__head Цена за токен
    tbody.table__body
      tr.table__row
        td.table__data userUser
          span.status.green--bg
        td.table__data Банковский перевод: Сбербанк
        td.table__data 0 - 10 000 ₽
        td.table__data 70,44 ₽
        td.table__data
          Button(rounded green) Купить
      tr.table__row
        td.table__data userUser
          span.status.green--bg
        td.table__data Банковский перевод: Сбербанк
        td.table__data 0 - 10 000 ₽
        td.table__data 70,44 ₽
        td.table__data
          Button(rounded green) Купить
      tr.table__row
        td.table__data userUser
          span.status.orange--bg
        td.table__data Банковский перевод: Сбербанк
        td.table__data 0 - 10 000 ₽
        td.table__data 70,44 ₽
        td.table__data
          Button(rounded green) Купить
      tr.table__row
        td.table__data userUser
          span.status.red--bg
        td.table__data Банковский перевод: Сбербанк
        td.table__data 0 - 10 000 ₽
        td.table__data 70,44 ₽
        td.table__data
          Button(rounded green) Купить
      tr.table__row
        td.table__data userUser
          span.status.green--bg
        td.table__data Банковский перевод: Сбербанк
        td.table__data 0 - 10 000 ₽
        td.table__data 70,44 ₽
        td.table__data
          Button(rounded green) Купить
</template>

<script>
import Button from '~/components/UI/Button'
export default {
  components: {
    Button
  },
  data() {
    return {
      tableData: [
        {
          seller: 'userUser',
          paymentMethod: 'Сбербанк',
          limit: '0 - 10 000 ₽',
          tokenPrice: '70,44 ₽'
        },
        {
          seller: 'userUser',
          paymentMethod: 'Сбербанк',
          limit: '0 - 10 000 ₽',
          tokenPrice: '70,44 ₽'
        },
        {
          seller: 'userUser',
          paymentMethod: 'Сбербанк',
          limit: '0 - 10 000 ₽',
          tokenPrice: '70,44 ₽'
        },
        {
          seller: 'userUser',
          paymentMethod: 'Сбербанк',
          limit: '0 - 10 000 ₽',
          tokenPrice: '70,44 ₽'
        }
      ]
    }
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
}
</style>
