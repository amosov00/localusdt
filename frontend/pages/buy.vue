<template>
  <section>
    <h1 class="table-section__title mt-330">Купить USDT</h1>
    <Tab :nav="false" :outsideParams="$route.query" :type="1" />
    <AppTable class="mb-80" :data="orders" :headers="headers" pagination>
      <template slot-scope="header"></template>
      <template slot-scope="{ row }">
        <td class="table__data">
          {{ row.username }}
          <span class="status green--bg" />
          <span class="orders-count">(10+)</span>
        </td>
        <td class="table__data">
          {{ paymentMethod(row.payment_method) }}
        </td>
        <td class="table__data">
          {{ spaceSplitting(row.bot_limit) }} -
          {{ spaceSplitting(row.top_limit) }} ₽
        </td>
        <td class="table__data">{{ commaSplitting(row.amount_usdt) }} USDT</td>
        <td class="table__data">{{ commaSplitting(row.price) }} ₽</td>
        <td class="table__data">
          <nuxt-link :to="`/order/${row._id}`">
            <Button rounded outlined green>Купить</Button>
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
      headers: [
        'Продавец',
        'Способ оплаты',
        'Лимит',
        'Количество',
        'Цена за токен'
      ]
    }
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
    return store.dispatch('order/fetchOrders', {
      limit: 1000,
      type: 2,
      sort: 1
    })
  }
}
</script>
