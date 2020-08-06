<template>
  <section>
    <h1 class="table-section__title mt-20">Продать USDT</h1>
    <Table :tableData="orders" />
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import Table from '~/components/app/Table'
export default {
  components: {
    Table
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
        ...query
      })
    }
    return store.dispatch('order/fetchOrders', { limit: 1000, type: 2 })
  }
}
</script>

<style></style>
