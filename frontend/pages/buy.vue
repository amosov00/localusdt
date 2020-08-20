<template>
  <section>
    <h1 class="table-section__title mt-330">Купить USDT</h1>
    <Tab :nav="false" :outsideParams="$route.query" :type="1" />
    <Table :tableData="orders" buttonName="Купить" />
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import Table from '~/components/app/Table'
import Tab from '~/components/Tab'
export default {
  components: {
    Table,
    Tab
  },
  computed: {
    ...mapGetters({
      orders: 'order/orders'
    })
  },
  asyncData({ store, query }) {
    const isQuery = Boolean(Object.keys(query).length)
    if (isQuery) {
      return store.dispatch('order/fetchOrders', {
        limit: 1000,
        type: 2,
        sort: -1,
        ...query
      })
    }
    return store.dispatch('order/fetchOrders', { limit: 1000, type: 2, sort: 1 })
  }
}
</script>

<style></style>
