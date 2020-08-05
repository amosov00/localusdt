<template lang="pug">
  div
    NonAuthorizedHero(v-if="!$userIsLoggedIn()")
    section.table-section
      h1.table-section__title Купить USDT
      Table(:tableData="sellOrders")
      nuxt-link(to="/buy")
        p.table-section__subtitle.fz-20 Показать больше объявлений
    section.table-section
      h1.table-section__title Продать USDT
      Table(:tableData="buyOrders")
      nuxt-link(to="/sell")
        p.table-section__subtitle.fz-20 Показать больше объявлений
</template>

<script>
import { mapGetters } from 'vuex'
import NonAuthorizedHero from '~/components/NonAuthorizedHero'
import SellBuyTab from '~/components/SellBuyTab'
import Table from '~/components/app/Table'
import Select from '~/components/app/Select'
export default {
  components: { NonAuthorizedHero, SellBuyTab, Table, Select },
  name: 'index',
  data() {
    return {
      options: [
        { name: 'RUB', value: 'rub' },
        { name: 'USD', value: 'usd' },
        { name: 'EUR', value: 'eur' }
      ],
      selected: 'Selected'
    }
  },
  computed: {
    ...mapGetters({
      sellOrders: 'order/sellOrders',
      buyOrders: 'order/buyOrders'
    })
  },
  methods: {
    selectedOption(option) {
      this.selected = option.name
    }
  },
  created() {
    this.$store.dispatch('order/fetchOrders')
  }
}
</script>

<style lang="scss">
.table-section {
  margin-top: 120px;
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
