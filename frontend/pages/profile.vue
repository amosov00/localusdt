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
        <p class="underline-link red" @click="logout()">{{$t('profile.logOut')}}</p>
      </div>
    </div>
    <div class="bio">
      <div class="bio__container">
        <h2 class="bio__title">{{$t('profile.about')}}</h2>
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
      <div class="tab-item" v-if="activeTab===1">
        <AppTable :data="invoices" :headers="headers" pagination>
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <td class="table__data">{{timestampToUtc(row.created_at)}}</td>
            <td class="table__data" v-if="row.ads_type === 1">{{$t('profile.sellUSDT')}}</td>
            <td class="table__data" v-else-if="row.ads_type === 2">{{$t('profile.buyUSDT')}}</td>
            <td class="table__data">
              {{ getUsername(row.seller_username, row.buyer_username)}}
              <span class="status green--bg" />
              <span class="orders-count">(10+)</span>
            </td>
            <td class="table__data">{{commaSplitting(row.amount_usdt)}}{{returnCurrency(row)}}
              <span class="grey-dark fw-400">
                {{$t('profile.for')}} {{commaSplitting(row.amount)}} USDT
              </span>
            </td>
            <td class="table__data" :style="{ color: statusColor(row.status) }">
              <nuxt-link :to="`/invoice/${row._id}`">{{invoiceStatusShort(row.status)}}</nuxt-link>
            </td>
          </template>
        </AppTable>
      </div>
      <div class="tab-item" v-if="activeTab===2">
        <AppTable :data="orders" :headers="orderHeaders" pagination>
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <td class="table__data">{{timestampToUtc(row.created_at)}}</td>
            <td class="table__data" v-if="row.type === 1">{{$t('profile.buyUSDT')}}</td>
            <td class="table__data" v-else-if="row.type === 2">{{$t('profile.sellUSDT')}}</td>
            <td class="table__data">{{commaSplitting(row.price)}}</td>
            <td class="table__data">
              <span>
                {{spaceSplitting(row.bot_limit)}} -
                {{spaceSplitting(row.top_limit)}} USDT
              </span>
            </td>
            <td class="table__data">{{spaceSplitting(row.amount_usdt)}}{{returnCurrency(row)}} USDT </td>
            <td class="table__data" :style="{ color: orderStatusColor(row.status) }">
              <nuxt-link :to="`/order/${row._id}`">{{orderStatus(row.status)}}</nuxt-link>
            </td>
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
      orderHeaders: [
        this.$t('profile.dateTime'),
        this.$t('profile.type'),
        this.$t('profile.course'),
        this.$t('profile.limit'),
        this.$t('profile.residue'),
        this.$t('profile.status'),
      ],
      headers: [
        this.$t('profile.dateTime'),
        this.$t('profile.orderType'),
        this.$t('profile.buyerSeller'),
        this.$t('profile.sum'),
        this.$t('profile.status'),
      ]
    }
  },
  created() {
    this.$store.dispatch('order/fetchOrdersByUser')
  },
  computed: {
    user() {
      return { ...this.$store.getters.user }
    },
    invoices() {
      console.log(this.$store.getters['invoice/invoices']);
      return this.$store.getters['invoice/invoices']
    },
    orders() {
      return [...this.$store.getters['order/ordersByUser']].reverse()
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
  asyncData({ store }) {
    return store.dispatch('invoice/fetchInvoices')
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
  }
}
</style>
