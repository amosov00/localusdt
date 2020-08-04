<template>
  <section>
    <h1 class="table-section__title mt-20">Купить USDT</h1>
    <Table :tableData="ads" />
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
      ads: 'ads/ads'
    })
  },
  asyncData({ store}) {
    return store.dispatch('ads/fetchAds', 2)
  },
}
</script>

<style>

</style>