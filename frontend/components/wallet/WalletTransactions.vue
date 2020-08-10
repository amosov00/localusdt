<template>
<div>
  <h2 class="fw-500 mt-50">История транзакций</h2>
  <table class="table">
    <thead class="table__header">
      <tr class="table__row">
        <th class="table__heade">Дата</th>
        <th class="table__heade">Действие</th>
        <th class="table__heade">Адрес</th>
        <th class="table__heade">Сумма</th>
        <th class="table__heade">Статус</th>
      </tr>
    </thead>
    <tbody class="table__body">
      <tr class="table__row">
        <td class="table__data"></td>
      </tr>
    </tbody>
  </table>
</div>
</template>

<script>
export default {

}
</script>

<style>
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
</style>