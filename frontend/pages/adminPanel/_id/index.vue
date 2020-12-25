<template>
  <div>
    <button class="backButton" @click="()=> this.$router.go(-1)">назад</button>
    <Tabs>
      <tab name="История сделок" :selected="true">
        <AppTable :data="invoices" :headers="headers" pagination>
          <template slot-scope="header"></template>
            <template slot-scope="{ row }">
              <td class="table__data">
                <p style="line-height:40px;">{{timestampToUtc(row.created_at)}}</p>
                <p style="font-size:10px; padding:0; line-height:15px;">ID сделки: {{row._id}}</p>
              </td>
              <td class="table__data" v-if="row.ads_type === 1">{{$t('profile.sellUSDT')}}</td>
              <td class="table__data" v-else-if="row.ads_type === 2">{{$t('profile.buyUSDT')}}</td>
              <td class="table__data">
                {{ row.seller_username}} / {{row.buyer_username}}
                <span class="status green--bg" />
                <span class="orders-count">(10+)</span>
              </td>
              <td class="table__data">
                <span class="grey-dark fw-400">
                  {{commaSplitting(row.amount_usdt)}} USDT {{$t('profile.for')}}
                </span>
                  {{commaSplitting(row.amount)}}{{returnCurrency(row)}}
              </td>
              <td class="table__data" :style="{ color: statusColor(row.status) }">
                <nuxt-link :to="`/adminPanel/${row._id}/invoice`">{{invoiceStatusShort(row.status)}}</nuxt-link>
              </td>
            </template>
        </AppTable>
      </tab>
      <tab name="Ваши обьявления">
        <AppTable :data="orders" :headers="orderHeaders" pagination>
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
            <td class="table__data">{{timestampToUtc(row.created_at)}}</td>
            <td class="table__data" v-if="row.type === 1">{{$t('profile.buyUSDT')}}</td>
            <td class="table__data" v-else-if="row.type === 2">{{$t('profile.sellUSDT')}}</td>
            <td class="table__data">{{commaSplitting(row.price)}} {{returnCurrency(row)}}</td>
            <td class="table__data">
              <span>
                {{spaceSplitting(row.bot_limit)}} -
                {{spaceSplitting(row.top_limit)}} USDT
              </span>
            </td>
            <td class="table__data">{{spaceSplitting(row.amount_usdt)}} USDT </td>
            <td class="table__data" :style="{ color: orderStatusColor(row.status) }">
              <nuxt-link :to="`/order/${row._id}`">{{orderStatus(row.status)}}</nuxt-link>
            </td>
          </template>
        </AppTable>
      </tab>
      <tab name="Вывод ввод">
        <AppTable :data="transactions" :headers="headersTransactions" pagination>
          <template slot-scope="header"></template>
          <template slot-scope="{ row }">
          <td class="table__data">{{timestampToUtc(row.date)}}</td>
          <td class="table__data">{{row.address}}</td>
          <td class="table__data">{{row.amount_usdt}}</td>
          <td class="table__data">{{row.event == 1 ? 'DEPOSIT' : 'WITHDRAW'}}</td>
          <td class="table__data">{{invoiceStatusNumber(row.status)}}</td>

          </template>
        </AppTable>
      </tab>
    </Tabs>
  </div>
</template>

<script>
import Tabs from '@/components/tabsAdminPanel/Tabs'
import Tab from '@/components/tabsAdminPanel/Tab'
import AppTable from '@/components/app/AppTable'
import formatCurreny from '~/mixins/formatCurrency'
import formatDate from '~/mixins/formatDate'
import invoiceStatuses from '~/mixins/invoiceStatuses'
import orderStatuses from '~/mixins/orderStatuses'

export default {
  mixins: [formatCurreny, formatDate, invoiceStatuses, orderStatuses],
  data(){
    return {
      headers: [
        this.$t('profile.dateTime'),
        this.$t('profile.buyerSeller'),
        this.$t('profile.sum'),
        this.$t('profile.status'),
      ],
      orderHeaders: [
        this.$t('profile.dateTime'),
        this.$t('profile.type'),
        this.$t('profile.course'),
        this.$t('profile.limit'),
        this.$t('profile.residue'),
        this.$t('profile.status'),
      ],
      headersTransactions: [
        this.$t('profile.dateTime'),
        this.$t('profile.address'),
        this.$t('profile.sum'),
        this.$t('profile.event'),
        this.$t('profile.status'),
      ]
    }
  },
  methods:{
    getUsername(seller, buyer) {
      const { username } = this.user
      return username === seller ? buyer : seller
    },
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
    }
  },
  computed:{
     user() {
      return { ...this.$store.getters.user }
    },
    invoices() {
      console.log(this.$store.getters['adminPanel/getAdminInvoices']);
      return  this.$store.getters['adminPanel/getAdminInvoices']
    },
    orders() {
      return this.$store.getters['adminPanel/getOrders']
    },
    transactions(){
      return this.$store.getters['adminPanel/geTransactions']
    }
  },
  components:{
    Tabs,
    Tab,
    AppTable
  },
  created(){
    this.$store.dispatch('adminPanel/getAdminInvoices', this.$route.params.id)
    this.$store.dispatch('adminPanel/byOrderUserId', this.$route.params.id)
    this.$store.dispatch('adminPanel/fetchIdTransactions', this.$route.params.id)
  },
}
</script>

<style>
.backButton{
margin-top: 10px;
border:none;
background-color: transparent;
color:#48B190;
cursor: pointer;
text-decoration: underline;
}
</style>
