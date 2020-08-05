<template>
  <section>
    <h1 class="table-section__title mt-20">Купить USDT</h1>
    <Table :tableData="orders" />
  </section>
</template>

<script>
import {mapGetters} from 'vuex'
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
  asyncData({ store}) {
    return store.dispatch('order/fetchOrders', 1)
  },
}
</script>

<style>

</style>