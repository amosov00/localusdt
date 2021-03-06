<template>
  <div>
    <h2 class="fw-500 mt-50">{{$t('wallet.transactionHistory')}}</h2>
    <AppTable class="mb-80" :incomingData="transactions" :headers="headers" :walletTX="true" pagination>
      <template slot-scope="{ row }">
          <component :is="rowsTag" class="table__data">
            <span class="text--grey" v-if="mobile">{{$t('wallet.date')}}: </span><span class="response-weight">{{regularDate(row.date)}}</span>
          </component>
          <component :is="rowsTag" class="table__data">
            <span class="text--grey" v-if="mobile">{{$t('wallet.action')}}: </span><span class="response-weight">{{ transactionEvent(row.event) }}</span>
          </component>
          <component :is="rowsTag" class="table__data address">
              <span class="text--grey" v-if="mobile">{{$t('wallet.address')}}: </span>
              <span class="response-weight">
                {{ row.address }}
              </span>
              <a
                class="ml-15"
                :href="`https://etherscan.io/address/${row.address}`"
                target="_blank"
                rel="noopener noreferrer"
              >
                <InlineSvg :src="require('~/assets/icons/redirect.svg')" />
              </a>
          </component>
          <component :is="rowsTag" class="table__data">
            <span class="text--grey" v-if="mobile">{{$t('wallet.amount')}}: </span>
            <span class="response-weight">{{ commaSplitting(row.amount_usdt) }} USDT</span>
          </component>
          <component
              class="table__data"
              :style="{ color: statusColor(row.status) }"
              :is="rowsTag"
          >
              <span class="text--grey" v-if="mobile">{{$t('wallet.status')}}: </span>
              <span class="response-weight">{{ transactionStatus(row.status) }}</span>
            </component>
      </template>
    </AppTable>
  </div>
</template>

<script>
import formatDate from '~/mixins/formatDate'
import formatCurrency from '~/mixins/formatCurrency'
import AppTable from '~/components/app/AppTable'
import InlineSvg from 'vue-inline-svg'
export default {
  mixins: [formatDate, formatCurrency],
  components: {
    InlineSvg,
    AppTable
  },
  data() {
    return {
      windowWidth: window.innerWidth,
    }
  },
  computed: {
    transactions() {
      return this.$store.getters['wallet/transactions'].map((item)=>{
        return {
          ...item,
          visible: false
        }
      })
    },
    mobile() {
      return this.windowWidth < 1100
    },
    headers() {
      if (this.windowWidth > 1100) {
        return [
          this.$t('wallet.date'),
          this.$t('wallet.action'),
          this.$t('wallet.address'),
          this.$t('wallet.amount'),
          this.$t('wallet.status')
        ]
      }
    },
    rowsTag() {
      if (this.windowWidth < 1100) {
        return 'div'
      } else {
        return 'td'
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
    transactionStatus(status) {
      switch (status) {
        case 1:
          return this.$t('wallet.done')
          break
        case 2:
          return this.$t('wallet.processed')
          break
        case 3:
          return this.$t('wallet.canceled')
          break
        default:
          break
      }
    },
    transactionEvent(event) {
      switch (event) {
        case 1:
          return this.$t('wallet.topUp2')
          break
        case 2:
          return this.$t('wallet.withdrawUSDT')
          break
        default:
          break
      }
    },
    statusColor(status) {
      switch (status) {
        case 1:
          return '#48B190'
          break
        case 2:
          return '#ED9F43'
          break
        case 3:
          return '#B31B11'
          break
      }
    }
  }
}
</script>
<style lang="scss">
  .address {
    word-break: break-all;
    padding-right: 30px;
  }
  div.table__data:not(:first-child) {
  @media (max-width: 1100px) {
    border-top: 1px solid grey;
  }
  }
</style>
