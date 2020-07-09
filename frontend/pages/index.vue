<template lang="pug">
  div
    NonAuthorizedHero
    SellBuyTab
    section.table-section
      h1.table-section__title Купить USDT
      Table
      p.table-section__subtitle Показать больше объявлений
    section.table-section
      h1.table-section__title Продать USDT
      Table
      p.table-section__subtitle Показать больше объявлений
</template>

<script>
import NonAuthorizedHero from '~/components/NonAuthorizedHero'
import SellBuyTab from '~/components/SellBuyTab'
import Table from '~/components/UI/Table'
export default {
  components: { NonAuthorizedHero, SellBuyTab, Table }
}
</script>

<style lang="scss">
.table-section {
  margin-top: 120px;
  margin-bottom: 120px;
  &__subtitle {
    margin-top: 30px;
    color: $orange;
    text-decoration: underline;
  }
}
</style>
