<template>
  <section>
    <Tab :nav="false" :outsideParams="$route.query" :type="1" />
    <h1 class="table-section__title">{{$t('main.sellUSDT')}}</h1>
    <AppTable class="mb-80" :data="orders" :headers="headers" pagination>
      <template slot-scope="header"></template>
      <template slot-scope="{ row }">
        <td class="table__data">
          {{ row.username }}
          <span class="status green--bg" />
        </td>
        <td class="table__data">
          {{ row.other_payment_method ? row.other_payment_method : paymentMethod(row.payment_method) }}
        </td>
        <td class="table__data" v-if="windowWidth > 998">
          {{ spaceSplitting(row.bot_limit) }} -
          {{ spaceSplitting(row.top_limit) }} USDT
        </td>
        <td
          class="table__data" v-if="windowWidth > 998">{{ commaSplitting(row.amount_usdt) }} USDT</td>
        <td
          class="table__data fw-500"
          :class="{center: windowWidth < 998}"
        >{{ commaSplitting(row.price) }} {{returnCurrency(row)}}
        </td>
        <td class="table__data" style="text-align: center">
          <nuxt-link :to="`/order/${row._id}`">
            <Button rounded outlined green v-if="windowWidth > 998">{{$t('main.sell')}}</Button>
            <img :src="require('@/assets/icons/shopping-cart.png')" alt="buy" v-if="windowWidth < 998">
          </nuxt-link>
        </td>
      </template>
    </AppTable>
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import Table from '~/components/app/Table'
import Tab from '~/components/Tab'
import AppTable from '~/components/app/AppTable'
import Button from '~/components/app/Button'
import paymentMethod from '~/mixins/paymentMethod'
import formatCurrency from '~/mixins/formatCurrency'
export default {
  mixins: [paymentMethod, formatCurrency],
  components: {
    Table,
    Tab,
    AppTable,
    Button
  },
  data() {
    return {
      windowWidth: window.innerWidth
    }
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', () => {
        this.windowWidth = window.innerWidth
      })
    })
  },
  methods:{
    returnCurrency(row){
      switch(row.currency){
        case 1:
         return '₽'
        break
        case 2:
          return 'Br'
        break
        case 3:
          return '$'
        break
        case 4:
          return '€'
        break
      }
    },
  },
  computed: {
    ...mapGetters({
      orders: 'order/orders'
    }),
    headers() {
      if (this.windowWidth > 998) {
        return [
          this.$t('main.seller'),
          this.$t('main.payType'),
          this.$t('main.limit'),
          this.$t('main.quantity'),
          this.$t('main.cost'),
        ]
      } else {
        return [
          this.$t('main.seller'),
          this.$t('main.payType'),
          this.$t('main.cost'),
        ]
      }
    }
  },
  asyncData({ store, query }) {
    const isQuery = Boolean(Object.keys(query).length)
    if (isQuery) {
      return store.dispatch('order/fetchOrders', {
        limit: 1000,
        type: 1,
        sort: -1,
        ...query
      })
    }
    return store.dispatch('order/fetchOrders', {
      limit: 1000,
      type: 1,
      sort: -1,
      currency:1
    })
  }
}
</script>
