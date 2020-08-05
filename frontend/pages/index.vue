<template lang="pug">
  div
    NonAuthorizedHero(v-if="!$userIsLoggedIn()")
    Tab(:top="top")
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
import Table from '~/components/app/Table'
import Tab from '~/components/Tab'
export default {
  components: { NonAuthorizedHero, Table, Tab },
  name: 'index',
  computed: {
    ...mapGetters({
      sellOrders: 'order/sellOrders',
      buyOrders: 'order/buyOrders'
    }),
    top() {
      if(!this.$userIsLoggedIn()) {
        return 300
      } else {
        return 100
      }
    }
  },
  methods: {
    selectedOption(option) {
      this.selected = option.name
    }
  },
  created() {
    this.$store.dispatch('order/fetchOrders', {limit: 5})
  }
}
</script>

<style lang="scss">
.table-section {
  margin-top: 320px;
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
