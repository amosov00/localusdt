<template>
  <div>
    <Slider/>
    <NonAuthorizedHero v-if="!$userIsLoggedIn()" />
    <Tab :top="top" @selectedTab="selectedOrders($event)" />
    <div v-if="!buyTab">
      <section class="table-section">
        <h1 class="table-section__title">{{ $t('main.buyUSDT') }}</h1>
        <AppTable :incomingData="sellOrdersWithLimit" :headers="[$t('main.seller'), ...headers]">
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <td class="table__data" :class="{'token_price-response': windowWidth < 565}">
              {{ row.username }}
              <span class="status green--bg" />
            </td>
            <td class="table__data" :class="{'payment_method-response': windowWidth < 565}">
              {{ row.other_payment_method ? row.other_payment_method : paymentMethod(row.payment_method) }}
            </td>
            <td class="table__data" v-if="windowWidth > 998">
              {{ spaceSplitting(row.bot_limit) }} -
              {{ spaceSplitting(row.top_limit) }} USDT
            </td>
            <td class="table__data" v-if="windowWidth > 998">
              {{ commaSplitting(row.amount_usdt) }} USDT
            </td>
            <td
              class="table__data fw-500"
              :class="[{center: windowWidth < 998}, {'token_price-response': windowWidth < 565}]"
            >{{ commaSplitting(row.price) }} {{returnCurrency(row)}}</td>
            <td class="table__data" style="text-align: center">
              <nuxt-link :to="`/order/${row._id}`">
                <Button rounded outlined green v-if="windowWidth > 998">{{ $t('main.sell') }}</Button>
                <img :src="require('@/assets/icons/shopping-cart.png')" alt="buy" v-if="windowWidth < 998">
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
        <AppTable :incomingData="buyOrdersWithLimit" :headers="[$t('main.buyer'), ...headers]">
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <td class="table__data" :class="{'token_price-response': windowWidth < 565}">
              {{ row.username }}
              <span class="status green--bg" />
            </td>
            <td class="table__data" :class="{'payment_method-response': windowWidth < 565}">
              {{ row.other_payment_method ? row.other_payment_method : paymentMethod(row.payment_method) }}
            </td>
            <td class="table__data" v-if="windowWidth > 998">
              {{ spaceSplitting(row.bot_limit) }} -
              {{ spaceSplitting(row.top_limit) }} USDT
            </td>
            <td class="table__data" v-if="windowWidth > 998">
              {{ commaSplitting(row.amount_usdt) }} USDT
            </td>
            <td
              class="table__data fw-500"
              :class="[{center: windowWidth < 998}, {'token_price-response': windowWidth < 565}]"
            >{{ commaSplitting(row.price) }} {{returnCurrency(row)}}</td>
            <td class="table__data" style="text-align: center">
              <nuxt-link :to="`/order/${row._id}`">
                <Button rounded outlined green v-if="windowWidth > 998">{{ $t('main.sell') }}</Button>
                <img :src="require('@/assets/icons/shopping-cart.png')" alt="buy" v-if="windowWidth < 998">
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
      <section class="table-section">
        <h1 class="table-section__title">{{ $t('main.sellUSDT') }}</h1>
        <AppTable :incomingData="buyOrdersWithLimit" :headers="[$t('main.buyer'), ...headers]">
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <td class="table__data" :class="{'token_price-response': windowWidth < 565}">
              {{ row.username }}
              <span class="status green--bg" />
            </td>
            <td class="table__data" :class="{'payment_method-response': windowWidth < 565}">
              {{ row.other_payment_method ? row.other_payment_method : paymentMethod(row.payment_method) }}
            </td>
            <td class="table__data" v-if="windowWidth > 998">
              {{ spaceSplitting(row.bot_limit) }} -
              {{ spaceSplitting(row.top_limit) }} USDT
            </td>
            <td class="table__data" v-if="windowWidth > 998">
              {{ commaSplitting(row.amount_usdt) }} USDT
            </td>
            <td
              class="table__data fw-500"
              :class="[{center: windowWidth < 998}, {'token_price-response': windowWidth < 565}]"
            >{{ commaSplitting(row.price) }} {{returnCurrency(row)}}</td>
            <td class="table__data" style="text-align: center">
              <nuxt-link :to="`/order/${row._id}`">
                <Button rounded outlined green v-if="windowWidth > 998">{{ $t('main.sell') }}</Button>
                <img :src="require('@/assets/icons/shopping-cart.png')" alt="buy" v-if="windowWidth < 998">
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
        <AppTable :incomingData="sellOrdersWithLimit" :headers="[$t('main.seller'), ...headers]">
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <td class="table__data" :class="{'token_price-response': windowWidth < 565}">
              {{ row.username }}
              <span class="status green--bg" />
            </td>
            <td class="table__data" :class="{'payment_method-response': windowWidth < 565}">
              {{ row.other_payment_method ? row.other_payment_method : paymentMethod(row.payment_method) }}
            </td>
            <td class="table__data" v-if="windowWidth > 998">
              {{ spaceSplitting(row.bot_limit) }} -
              {{ spaceSplitting(row.top_limit) }} USDT
            </td>
            <td class="table__data" v-if="windowWidth > 998">
              {{ commaSplitting(row.amount_usdt) }} USDT
            </td>
            <td
              class="table__data fw-500"
              :class="[{center: windowWidth < 998}, {'token_price-response': windowWidth < 565}]"
            >
              {{ commaSplitting(row.price) }} {{returnCurrency(row)}}
            </td>
            <td class="table__data" style="text-align: center">
              <nuxt-link :to="`/order/${row._id}`">
                <Button rounded outlined green v-if="windowWidth > 998">{{ $t('main.sell') }}</Button>
                <img :src="require('@/assets/icons/shopping-cart.png')" alt="buy" v-if="windowWidth < 998">
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
import Slider from '@/components/app/SwiperSlider'
import Button from '~/components/app/Button'

export default {
  mixins: [paymentMethod, formatCurrency],
  components: { NonAuthorizedHero, Table, Tab, AppTable, Button ,Slider},
  name: 'index',
  data() {
    return {
      buyTab: true,
      sellTab: false,
      windowWidth: window.innerWidth
    }
  },
  computed: {
    swiper() {
        return this.$refs.mySwiper.$swiper
    },
    headers() {
      if (this.windowWidth > 998) {
        return [
          this.$t('main.payType'),
          this.$t('main.limit'),
          this.$t('main.quantity'),
          this.$t('main.cost'),
        ]
      } else {
        return [
          this.$t('main.payType'),
          this.$t('main.cost'),
        ]
      }
    },
    top() {
      let top = 316
      if (!this.$userIsLoggedIn()) {
        top = 516
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
  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', () => {
        this.windowWidth = window.innerWidth
      })
    })
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
  async asyncData({ store }) {
    await store.dispatch('order/fetchOrders', {
      limit: 1000,
      sort: -1,
      currency:1
    })
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
[alt="buy"] {
  width: 20px;
}
</style>
