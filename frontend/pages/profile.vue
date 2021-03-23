<template>
  <section class="profile">
    <div class="profile__header">
      <div class="profile__user">
        <h1 class="profile__username">
          {{ user.username }}
        </h1>
        <span class="profile__activity"></span>
      </div>
      <div class="profile__actions">
        <nuxt-link class="underline-link underline-link--grey" to="/change">
          {{$t('profile.changePass')}}
        </nuxt-link>
        <nuxt-link v-if="$userIsStaff()" class="underline-link underline-link--grey" to="/adminPanel">
          {{$t('profile.adminPanel')}}
        </nuxt-link>
        <p class="underline-link red" @click="logout()">{{$t('profile.logOut')}}</p>
      </div>

    </div>
    <div class="bio">
      <div class="bio__container">
        <h3 class="bio__title">{{$t('profile.about')}}</h3>
        <Textarea v-model="condition" />
        <Button @click.native="setCondition" class="mt-20" green>
          {{$t('profile.save')}}
        </Button>
      </div>
      <ProfileReferral />
    </div>
    <div class="tab" :style="{ top: '0' }">
      <nav class="tab-nav">
        <div
          class="tab-nav__item"
          @click="setTab(1)"
          :class="{ 'tab-nav__item--active': activeTab === 1 }"
        >
          {{$t('profile.history')}}
        </div>
        <div
          class="tab-nav__item"
          @click="setTab(2)"
          :class="{ 'tab-nav__item--active': activeTab === 2 }"
        >
          {{$t('profile.orders')}}
        </div>
      </nav>
      <div class="tab-item" v-show="activeTab===1">
        <AppTable :incomingData="invoices" :headers="headers" pagination :walletTX="true">
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <component :is="rowsTag" class="table__data">
              <p style="line-height:40px;">{{timestampToUtc(row.created_at)}}</p>
              <p style="font-size:10px; padding:0; line-height:15px;">ID сделки: {{row._id}}</p>
            </component>
            <component :is="rowsTag" class="table__data" v-if="row.seller_username === user.username">{{$t('profile.sellUSDT')}}</component>
            <component :is="rowsTag" class="table__data" v-else>{{$t('profile.buyUSDT')}}</component>
            <component :is="rowsTag" class="table__data">
              {{ getUsername(row.seller_username, row.buyer_username)}}
              <span class="status green--bg" />
              <span class="orders-count">(10+)</span>
            </component>
            <component :is="rowsTag" class="table__data">
               <span class="grey-dark fw-400">
                 {{commaSplitting(row.amount_usdt)}} USDT {{$t('profile.for')}}
              </span>
                {{commaSplitting(row.amount)}}{{returnCurrency(row)}}
            </component>
            <component :is="rowsTag" class="table__data" :style="{ color: statusColor(row.status) }">
              <nuxt-link :to="`/invoice/${row._id}`">{{invoiceStatusShort(row.status)}}</nuxt-link>
            </component>
          </template>
        </AppTable>
      </div>
      <div class="tab-item" v-show="activeTab===2">
        <AppTable :incomingData="orders" :headers="orderHeaders" pagination :walletTX="true">
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <component :is="rowsTag" class="table__data">
              <span class="text--grey" v-if="mobile">{{$t('profile.dateTime')}}: </span><b>{{timestampToUtc(row.created_at)}}</b>
            </component>
            <component :is="rowsTag" class="table__data" v-if="row.type === 1">
              <span class="text--grey" v-if="mobile">{{$t('profile.type')}}: </span><b>{{$t('profile.buyUSDT')}}</b>
            </component>
            <component :is="rowsTag" class="table__data" v-else-if="row.type === 2">
              <span class="text--grey" v-if="mobile">{{$t('profile.type')}}: </span><b>{{$t('profile.sellUSDT')}}</b>
            </component>
            <component :is="rowsTag" class="table__data">
              <span class="text--grey" v-if="mobile">{{$t('profile.course')}}: </span><b>{{commaSplitting(row.price)}} {{returnCurrency(row)}}</b>
            </component>
            <component :is="rowsTag" class="table__data">
              <span class="text--grey" v-if="mobile">{{$t('profile.limit')}}: </span>
              <b>
                {{spaceSplitting(row.bot_limit)}} -
                {{spaceSplitting(row.top_limit)}} USDT
              </b>
            </component>
            <component :is="rowsTag" class="table__data">
              <span class="text--grey" v-if="mobile">{{$t('profile.residue')}}: </span><b>{{spaceSplitting(row.amount_usdt)}} USDT</b>
            </component>
            <component :is="rowsTag" class="table__data" :style="{ color: orderStatusColor(row.status) }">
              <span class="text--grey" v-if="mobile">{{$t('profile.status')}}: </span><nuxt-link :to="`/order/${row._id}`"><b>{{orderStatus(row.status)}}</b></nuxt-link>
            </component>
          </template>
        </AppTable>
      </div>
    </div>
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import ProfileReferral from '~/components/ProfileReferral'
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
import AppTable from '~/components/app/AppTable'
import formatCurreny from '~/mixins/formatCurrency'
import formatDate from '~/mixins/formatDate'
import invoiceStatuses from '~/mixins/invoiceStatuses'
import orderStatuses from '~/mixins/orderStatuses'

export default {
  name: 'profile',
  middleware: ['authRequired', 'fetchUser'],
  mixins: [formatCurreny, formatDate, invoiceStatuses, orderStatuses],
  components: {
    ProfileReferral,
    Textarea,
    Button,
    AppTable
  },
  data() {
    return {
      activeTab: 1,
      windowWidth: window.innerWidth,
    }
  },
  created() {
    this.$store.dispatch('order/fetchOrdersByUser')
  },
  computed: {
    rowsTag() {
      if (this.windowWidth < 1100) {
        return 'div'
      } else {
        return 'td'
      }
    },
    mobile() {
      return this.windowWidth < 1100
    },
    orderHeaders() {
      if (this.windowWidth > 1100) {
        return [
          this.$t('profile.dateTime'),
          this.$t('profile.type'),
          this.$t('profile.course'),
          this.$t('profile.limit'),
          this.$t('profile.residue'),
          this.$t('profile.status')
        ]
      }
    },
    headers() {
      if (this.windowWidth > 1100) {
        return [
          this.$t('profile.dateTime'),
          this.$t('profile.orderType'),
          this.$t('profile.buyerSeller'),
          this.$t('profile.sum'),
          this.$t('profile.status'),
        ]
      }
    },
    user() {
      return { ...this.$store.getters.user }
    },
    invoices() {
      return this.$store.getters['invoice/invoices'].map((item)=>{
        let type
        if (item.seller_username === this.user.username) {
          type = 2
        } else {
          type = 1
        }
        return {
          ...item,
          type,
          visible: false
        }
      })
    },
    orders() {
      return [...this.$store.getters['order/ordersByUser']].reverse().map((item)=>{
        return {
          ...item,
          visible: false
        }
      })
    },
    condition: {
      get: function() {
        return this.user.about_me
      },
      set: function(value) {
        this.user.about_me = value
      }
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
    getUsername(seller, buyer) {
      const { username } = this.user
      return username === seller ? buyer : seller
    },
    setTab(tab) {
      this.activeTab = tab
    },
    logout() {
      this.$store.dispatch('logOut')
    },
    setCondition() {
      this.$store.dispatch('changeCondition', this.user.about_me)
    }
  },
  async asyncData({ store }) {
    await store.dispatch('invoice/fetchInvoices')
    await store.dispatch('order/fetchOrdersByUser')
  }
}
</script>

<style lang="scss">
.profile {
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 50px;
    padding-bottom: 40px;
    border-bottom: 1px solid $grey;
  }

  &__user {
    display: flex;
    align-items: center;
  }

  &__activity {
    display: block;
    margin-left: 20px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background-color: $green;
  }

  &__actions {
    display: flex;
    flex-direction: column;
    text-align: right;
  }

  .bio {
    margin-top: 50px;
    display: flex;
    justify-content: space-between;
    @media (max-width: 966px) {
      display: block;
      &__container {
        margin-bottom: 40px;
      }
    }

    &__title {
      margin-bottom: 35px;
      font-weight: 500;
    }
  }
}
</style>

<style lang="scss" scoped>

.tab {
  position: relative;

  &-item {
    background-color: #fdfdfd;
    border: 1px solid #f3f3f3;
    margin-top: -1px;
    padding-right: 20px;
    padding-left: 20px;
  }
}

div.table__data:not(:first-child) {
  @media (max-width: 1100px) {
    border-top: 1px solid grey;
  }
}
</style>
