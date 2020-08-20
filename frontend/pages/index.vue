<template lang="pug">
  div
    NonAuthorizedHero(v-if="!$userIsLoggedIn()")
    Tab(:top="top" @selectedTab="selectedOrders($event)")
    div(v-if="buyTab")
      section.table-section.mt-330
        h1.table-section__title Купить USDT
        Table(:tableData="buyOrdersWithLimit" buttonName="Купить")
        nuxt-link(to="/buy")
          p.table-section__subtitle.fz-20 Показать больше объявлений
      section.table-section
        h1.table-section__title Продать USDT
        Table(:tableData="sellOrdersWithLimit" buttonName="Продать")
        nuxt-link(to="/sell")
          p.table-section__subtitle.fz-20 Показать больше объявлений
    div(v-else)
      section.table-section.mt-330
        h1.table-section__title Продать USDT
        Table(:tableData="sellOrdersWithLimit" buttonName="Продать")
        nuxt-link(to="/sell")
          p.table-section__subtitle.fz-20 Показать больше объявлений
      section.table-section
        h1.table-section__title Купить USDT
        Table(:tableData="buyOrdersWithLimit" buttonName="Купить")
        nuxt-link(to="/buy")
          p.table-section__subtitle.fz-20 Показать больше объявлений
</template>

<script>
import NonAuthorizedHero from '~/components/NonAuthorizedHero'
import Table from '~/components/app/Table'
import Tab from '~/components/Tab'
export default {
  components: { NonAuthorizedHero, Table, Tab },
  name: 'index',
  data() {
    return {
      buyTab: true,
      sellTab: false,
    }
  },
  computed: {
    top() {
      if(!this.$userIsLoggedIn()) {
        return 300
      } else {
        return 100
      }
    },
    buyOrdersWithLimit() {
      return this.$store.getters['order/buyOrdersWithLimit'](5)
    },
    sellOrdersWithLimit() {
      return this.$store.getters['order/sellOrdersWithLimit'](5)
    }
  },
  methods: {
    selectedOption(option) {
      this.selected = option.name
    },
    selectedOrders(tabs) {
      this.buyTab = tabs.buy
      this.sellTab = tabs.sell
    }
  },
  created() {
    this.$store.dispatch('order/fetchOrders', {limit: 1000})
  }
}
</script>

<style lang="scss">
.table-section {
  margin-bottom: 120px;
  &__subtitle {
    @include montserrat;
    font-size: 16px;
    margin-top: 30px;
    color: $orange;
    text-decoration: underline;
  }
}
</style>
