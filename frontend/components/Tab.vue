<template>
  <div class="tab" :style="{ top: `${top}px` }">
    <nav v-if="nav" class="tab-nav">
      <div
        class="tab-nav__item"
        :class="{ 'tab-nav__item--active':  secondTab  }"
        @click="selectTab"
      >
        {{ $t('main.fastBuy') }}
      </div>
      <div
        class="tab-nav__item"
        :class="{ 'tab-nav__item--active': firstTab }"
        @click="selectTab"
      >
        {{ $t('main.fastSell') }}
      </div>
    </nav>
    <div class="tab-body">
      <Input
        v-model="searchForm.bot_limit"
        type="number"
        :header="$t('main.cost')"
        placeholder="0,00"
        class="tab-body__item"
      />
      <Input
        v-model="searchForm.top_limit"
        type="number"
        placeholder="0,00"
        class="tab-body__item"
      />
      <Select
        v-model="searchForm.currency"
        :options="currencyOptions"
        :selectedOptionProp="outsideParams ? outsideParams.currency : '1'"
        class="tab-body__item tab-body__currency"
      />
      <Select
        v-model="searchForm.payment_method"
        :options="paymentOptions"
        noCurrency
        :selectedOptionProp="outsideParams ?  outsideParams.payment_method ? outsideParams.payment_method : '5' : '5'"
        class="tab-body__item tab-body__payment_method"
      />
      <Button green @click.native="searchOrders" class="tab-body__item tab-body__button"> {{ $t('main.search') }}</Button>
    </div>
  </div>
</template>

<script>
import Input from '~/components/app/Input'
import Select from '~/components/app/Select'
import Button from '~/components/app/Button'

export default {
  props: {
    top: Number,
    outsideParams: Object,
    nav: {
      type: Boolean,
      default: true
    },
    type: Number
  },
  components: {
    Input,
    Select,
    Button
  },
  data() {
    return {
      searchForm: {
        payment_method: this.outsideParams &&  this.outsideParams.payment_method !== undefined ? this.outsideParams.payment_method : 5,
        currency: this.outsideParams &&  this.outsideParams.currency !== undefined ? (this.outsideParams.currency) : 1,
        bot_limit: this.outsideParams &&  this.outsideParams.price_bot !== undefined ? this.outsideParams.price_bot : 0,
        top_limit: this.outsideParams &&  this.outsideParams.price_top !== undefined ? this.outsideParams.price_top : 0,
      },
      firstTab: true,
      secondTab: false,
      currencyOptions: [
        { name: 'RUB', value: 1 },
        { name: 'BYN', value: 2 },
        { name: 'USD', value: 3 },
        { name: 'EUR', value: 4 }
      ],
      paymentOptions: [
        { name: `${this.$t('main.bankTransfer')} ${this.$t('main.sberbank')}`, value: 1 },
        { name: `${this.$t('main.bankTransfer')} ${this.$t('main.tinkof')}`, value: 2, selected: true },
        { name: `${this.$t('main.bankTransfer')} ${this.$t('main.alfa')}`, value: 3 },
        { name: this.$t('main.otherWay'), value: 4 },
        { name: `${this.$t('main.all')}`, value: 5 },
        { name: `${this.$t('main.bankTransfer')} ${this.$t('main.cardToCard')}`, value: 6 },
        { name: `${this.$t('main.qiwi')}`, value: 7 },
        { name: `${this.$t('main.yandex')}`, value: 8 },
        { name: `${this.$t('main.payeer')}`, value: 9 },
        { name: `${this.$t('main.payPal')}`, value: 10 },
        { name: `${this.$t('main.cash')}`, value: 11 },
        { name: `${this.$t('main.webMoney')}`, value: 12 },
      ]
    }
  },
  computed: {
    routePath() {
      if (this.type === 1 || this.firstTab) {
        return '/sell'
      } else {
        return '/buy'
      }
    },
    queries() {
      return `/?${this.searchForm.payment_method == 5 ? '' : `payment_method=${this.searchForm.payment_method}`}&currency=${this.searchForm.currency}&price_bot=${this.searchForm.bot_limit}&price_top=${this.searchForm.top_limit}`
    },
    adType() {
      if (this.firstTab || this.type === 1) {
        return 1
      } else {
        return 2
      }
    }
  },
  mounted(){
    if(this.$route.path == '/') return
    if(this.$route.path == '/buy') this.firstTab = false
    if(this.$route.path == '/sell'){
      this.firstTab = true
      console.log(this.type);
    }
  },
  methods: {
    selectTab() {
      if (this.firstTab) {
        this.secondTab = true
        this.firstTab = false
      } else {
        this.secondTab = false
        this.firstTab = true
      }
      this.$emit('selectedTab', { buy: this.firstTab, sell: this.secondTab })
    },
    searchOrders() {
      this.$store.dispatch('order/searchOrders', {
        ...this.searchForm,
        ad_type: this.adType
      })
      this.$router.push(this.routePath + this.queries)
    }
  }
}
</script>

<style lang="scss">
.tab {
  width: 100%;
  transition: all .5s;
  max-width: 1200px;
  margin: 70px auto 70px auto;

  .tab-nav {
    display: flex;
    justify-content: center;
    @include montserrat;

    &__item {
      padding: 25px;
      cursor: pointer;
      border: 1px solid transparent;
      border-radius: 6px 6px 0px 0px;
      opacity: 0.5;

      &:first-child {
        margin-right: 30px;
      }

      &--active {
        border: 1px solid #f3f3f3;
        border-bottom: none;
        background-color: #fdfdfd;
        opacity: 1;
      }
    }
  }

  .tab-body {
    background-color: #fdfdfd;
    border: 1px solid #f3f3f3;
    height: 150px;
    margin-top: -1px;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding-top: 50px;
    @media (max-width: 916px) {
      display: block;
      height: auto;
      &__item {
        margin-bottom: 20px;
      }
    }
    .tab-body__currency {
      width: 80px;
      @media (max-width: 916px) {
        width: auto;
      }
    }

    .tab-body__payment_method {
      width: 370px;
      @media (max-width: 916px) {
        width: auto;
      }
    }

    & > * {
      margin-left: 25px;
      @media (max-width: 916px) {
        margin-right: 25px;
      }
      &:last-child {
        margin-left: 70px;
        @media (max-width: 916px) {
          margin-left: 25px;
          display: block;
        }
      }
    }
  }
}
</style>
