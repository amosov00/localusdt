<template>
  <div>
    <NonAuthorizedHero v-if="!$userIsLoggedIn()" />
    <Tab :top="top" @selectedTab="selectedOrders($event)" />
    <div v-if="!buyTab">
      <section class="table-section mt-330">
        <h1 class="table-section__title">{{ $t('main.buyUSDT') }}</h1>
        <AppTable :data="sellOrdersWithLimit" :headers="[$t('main.seller'), ...headers]">
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <td class="table__data">
              {{ row.username }}
              <span class="status green--bg" />
              <span class="orders-count">(10+)</span>
            </td>
            <td class="table__data">
              {{ row.other_payment_method ? row.other_payment_method : paymentMethod(row.payment_method) }}
            </td>
            <td class="table__data">
              {{ spaceSplitting(row.bot_limit) }} -
              {{ spaceSplitting(row.top_limit) }} USDT
            </td>
            <td class="table__data">
              {{ commaSplitting(row.amount_usdt) }} USDT
            </td>
            <td class="table__data fw-500">{{ commaSplitting(row.price) }} ₽</td>
            <td class="table__data">
              <nuxt-link :to="`/order/${row._id}`">
                <Button rounded outlined green>{{ $t('main.buy') }}</Button>
              </nuxt-link>
            </td>
          </template>
        </AppTable>
        <nuxt-link to="buy/">
          <p class="table-section__subtitle fz-20 ">
            {{ $t('main.showMore') }}
          </p>
        </nuxt-link>
      </section>
      <section class="table-section">
        <h1 class="table-section__title">{{ $t('main.sellUSDT') }}</h1>
        <AppTable :data="buyOrdersWithLimit" :headers="[$t('main.buyer'), ...headers]">
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <td class="table__data">
              {{ row.username }}
              <span class="status green--bg" />
              <span class="orders-count">(10+)</span>
            </td>
            <td class="table__data">
              {{ row.other_payment_method ? row.other_payment_method : paymentMethod(row.payment_method) }}
            </td>
            <td class="table__data">
              {{ spaceSplitting(row.bot_limit) }} -
              {{ spaceSplitting(row.top_limit) }} USDT
            </td>
            <td class="table__data">
              {{ commaSplitting(row.amount_usdt) }} USDT
            </td>
            <td class="table__data fw-500">{{ commaSplitting(row.price) }} {{returnCurrency(row)}}</td>
            <td class="table__data">
              <nuxt-link :to="`/order/${row._id}`">
                <Button rounded outlined green>{{ $t('main.sell') }}</Button>
              </nuxt-link>
            </td>
          </template>
        </AppTable>
        <nuxt-link to="sell/">
          <p class="table-section__subtitle fz-20 ">
            {{ $t('main.showMore') }}
          </p>
        </nuxt-link>
      </section>
    </div>
    <div v-else>
      <section class="table-section mt-330">
        <h1 class="table-section__title">{{ $t('main.sellUSDT') }}</h1>
        <AppTable :data="buyOrdersWithLimit" :headers="[$t('main.buyer'), ...headers]">
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <td class="table__data">
              {{ row.username }}
              <span class="status green--bg" />
              <span class="orders-count">(10+)</span>
            </td>
            <td class="table__data">
              {{ row.other_payment_method ? row.other_payment_method : paymentMethod(row.payment_method) }}
            </td>
            <td class="table__data">
              {{ spaceSplitting(row.bot_limit) }} -
              {{ spaceSplitting(row.top_limit) }} USDT
            </td>
            <td class="table__data">
              {{ commaSplitting(row.amount_usdt) }} USDT
            </td>
            <td class="table__data fw-500">{{ commaSplitting(row.price) }}₽</td>
            <td class="table__data">
              <nuxt-link :to="`/order/${row._id}`">
                <Button rounded outlined green>{{ $t('main.sell') }}</Button>
              </nuxt-link>
            </td>
          </template>
        </AppTable>
        <nuxt-link to="sell/">
          <p class="table-section__subtitle fz-20 ">
            {{ $t('main.showMore') }}
          </p>
        </nuxt-link>
      </section>
      <section class="table-section">
        <h1 class="table-section__title">{{ $t('main.buyUSDT') }}</h1>
        <AppTable :data="sellOrdersWithLimit" :headers="[$t('main.seller'), ...headers]">
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <td class="table__data">
              {{ row.username }}
              <span class="status green--bg" />
              <span class="orders-count">(10+)</span>
            </td>
            <td class="table__data">
              {{ row.other_payment_method ? row.other_payment_method : paymentMethod(row.payment_method) }}
            </td>
            <td class="table__data">
              {{ spaceSplitting(row.bot_limit) }} -
              {{ spaceSplitting(row.top_limit) }} USDT
            </td>
            <td class="table__data">
              {{ commaSplitting(row.amount_usdt) }} USDT
            </td>
            <td class="table__data fw-500">{{ commaSplitting(row.price) }} ₽</td>
            <td class="table__data">
              <nuxt-link :to="`/order/${row._id}`">
                <Button rounded outlined green>{{ $t('main.buy') }}</Button>
              </nuxt-link>
            </td>
          </template>
        </AppTable>
        <nuxt-link to="buy/">
          <p class="table-section__subtitle fz-20 ">
            {{ $t('main.showMore') }}
          </p>
        </nuxt-link>
      </section>
    </div>
  </div>
</template>

<script>
import NonAuthorizedHero from '~/components/NonAuthorizedHero'
import Table from '~/components/app/Table'
import Tab from '~/components/Tab'
import AppTable from '~/components/app/AppTable'
import paymentMethod from '~/mixins/paymentMethod'
import formatCurrency from '~/mixins/formatCurrency'
import Button from '~/components/app/Button'
import Vue from 'vue'

export default {
  mixins: [paymentMethod, formatCurrency],
  components: { NonAuthorizedHero, Table, Tab, AppTable, Button },
  name: 'index',
  data() {
    return {
      buyTab: true,
      sellTab: false,
      headers: [
        this.$t('main.payType'),
        this.$t('main.limit'),
        this.$t('main.quantity'),
        this.$t('main.cost'),
      ]
    }
  },
  computed: {
    top() {
      let top = 100
      if (!this.$userIsLoggedIn()) {
        top = 300
      }
      return this.isToastActive ? top + 50 : top
    },
    buyOrdersWithLimit() {
      return this.$store.getters['order/buyOrdersWithLimit'](5);
    },
    sellOrdersWithLimit() {
      return this.$store.getters['order/sellOrdersWithLimit'](5)
    },
    isToastActive() {
      return this.$store.getters['toast/isActive']
    }
  },
  methods: {
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
    selectedOption(option) {
      this.selected = option.name
    },
    selectedOrders(tabs) {
      this.buyTab = tabs.buy
      this.sellTab = tabs.sell
    }
  },
  created() {
    this.$store.dispatch('order/fetchOrders', { limit: 1000, })
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
