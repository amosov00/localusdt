<template lang="pug">
div.bid-type
  header.bid-type__header
    h1.bid-type__title Что Вы хотите?
    p.paragraph-1.bid-type__subtitle Выберите тип сделки
  div.bid-type__body
    nuxt-link.bid-type__link(to="/bid/sell/")
      img(src="~/assets/icons/sell-bid.svg")
    nuxt-link.bid-type__link(to="/bid/buy/")
      img(src="~/assets/icons/buy-bid.svg")
</template>

<script>
export default {
  middleware: ['authRequired']
}
</script>

<style lang="scss">
.bid-type {
  margin: 0 auto;
  max-width: 500px;
  width: 100%;
  text-align: center;
  padding-top: 130px;

  &__header {
    margin-bottom: 90px;
  }

  &__link {
    @include reset-link;
    height: 180px;
    width: 160px;
  }

  &__body {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
}
</style>
