<template lang="pug">
  div.create-order

    header.create-order__navigation
      h1 {{$t('bid.buyUSDT')}}
    hr
    div.create-order__form
      div.create-order__options
        Select(
        :options="paymentOptions"
        :selectedOptionProp="adForm.payment_method"
        v-model="adForm.payment_method"
        :width="350"
        noCurrency
        :header="$t('bid.payType')"
        )
        Select(
        :options="currencyOptions"
        v-model="adForm.currency"
        :width="80"
        @defaultProfit="resetProfit"
        profitForm
        :header="$t('bid.currency')"
        hideArrow)
      Input.create-order__input(
      v-if="yourVersion"
      v-model="adForm.bank_title"
      header=""
      :placeholder="$t('bid.otherVariant')"
      )

      Input.create-order__input.mt-40.mb-110(
      v-model="adForm.amount_usdt"
      type="number"
      :header="inputHeader"
      placeholder="0"
      endIcon="usdt")

      h2.create-order-price {{$t('bid.price')}}:
      div.radio-group
        label(for="profit-is-formula")
          input(id="profit-is-formula"
          type="radio"
          value="formula"
          name="profit-mode"
          @click="defaultRate"
          v-model="profitMode")
          span {{$t('bid.formula')}}
        label(for="profit-is-fixed")
          input(
          id="profit-is-fixed"
          type="radio"
          value="fixed"
          name="profit-mode"
          @click="defaultRate"
          v-model="profitMode")
          span {{$t('bid.fixed')}}
      Input.create-order__input(
      v-model="adForm.price"

      :header="$t('bid.price')"
      :placeholder="$t('bid.price')"
      v-if="adForm.fixed_price")
      Input.create-order__input(
      v-model="adForm.profit"
      @input="editTokenPrice"
      @keydown.native.delete="keyPressBackspace"
      :header="$t('bid.profit')"
      :placeholder="$t('bid.profit')"
      type="number"
      endIcon="procent"
      hint
      v-if="!adForm.fixed_price")

      Input.create-order__input(
      disabled
      :value="equation"
      :header="$t('bid.priceSetting')"
      type="text"
      hintTwo
      :typeCurrency="currencyFullData.type"
      v-if="profitMode === 'formula'")
      p.create-order__token-price {{$t('bid.actualCourse')}}
        =' '
        span.green(v-if="actualPrice") {{ commaSplitting(actualPrice)}}
        span {{ returnCurrency }}/USDT
      div.create-order__gap
        Input.mr-30(
        v-model="adForm.bot_limit"
        :width="250"
        type="number"
        :header="$t('bid.minLimit')")

        Input(
        v-model="adForm.top_limit"
        :width="250"
        type="number"
        :header="$t('bid.maxLimit')")
        span.extra-text USDT
      Textarea.create-order__conditions(
      v-model="adForm.condition"
      :placeholder="$t('bid.writeTerms')")

      Checkbox(v-model="checkbox" :label="$t('bid.putProfileTerms')")
      Button.create-order__action(green @click.native="createAd(false)" v-if="!editMode") {{$t('bid.createAd')}}
      div(v-else).create-order__action
        Button(green @click.native="createAd(true)").mr-15 {{$t('bid.save')}}
        Button(white @click.native="$nuxt.context.redirect(`/order/${$route.query.edit}`)")  {{$t('bid.cancel')}}
      Modal(:show="showModal" @toggleModal="toggleModal($event)" :type="1")
</template>

<script>
import Input from '~/components/app/Input'
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
import Checkbox from '~/components/app/Checkbox'
import Select from '~/components/app/Select'
import Modal from '~/components/app/Modal'
import { mapGetters } from 'vuex'
import formatCurrency from '~/mixins/formatCurrency'

export default {
  components: { Input, Textarea, Button, Checkbox, Select, Modal },
  middleware: ['authRequired'],
  mixins: [formatCurrency],

  data() {
    return {
      editMode: false,
      profitMode: 'formula',
      adForm: {
        type: 1,
        bot_limit: null,
        top_limit: null,
        amount_usdt: null,
        payment_method: 1,
        bank_title: '',
        currency: 1,
        condition: '',
        profit: 0,
        fixed_price: false,
        price: 0
      },
      currencyOptions: [
        { name: 'RUB', value: 1 },
        { name: 'BYN', value: 2 },
        { name: 'USD', value: 3 },
        { name: 'EUR', value: 4 }
      ],
      paymentOptions: [
        { name: `${this.$t('main.bankTransfer')} ${this.$t('main.sberbank')}`, value: 1 },
        { name: `${this.$t('main.bankTransfer')} ${this.$t('main.tinkof')}`, value: 2,  },
        { name: `${this.$t('main.bankTransfer')} ${this.$t('main.alfa')}`, value: 3 },
        { name: this.$t('main.otherWay'), value: 4,selected: true},
        { name: `${this.$t('main.all')}`, value: 5 },
        { name: `${this.$t('main.bankTransfer')} ${this.$t('main.cardToCard')}`, value: 6 },
        { name: `${this.$t('main.qiwi')}`, value: 7 },
        { name: `${this.$t('main.yandex')}`, value: 8 },
        { name: `${this.$t('main.payeer')}`, value: 9 },
        { name: `${this.$t('main.payPal')}`, value: 10 },
        { name: `${this.$t('main.cash')}`, value: 11 },
        { name: `${this.$t('main.webMoney')}`, value: 12 },
      ],
      showModal: false,
      checkbox: false,
      actualPrice: null
    }
  },
  watch: {
    currencyPrice(){
      this.actualPrice = this.currencyPrice
    },
    profitMode() {
      if (this.profitMode === 'fixed') {
        this.adForm.fixed_price = true
        this.adForm.price = this.currencyPrice.toFixed(2)
      } else {
        this.adForm.fixed_price = false
        this.adForm.price = 0
      }
    },
    checkbox: function() {
      if (this.checkbox) {
        this.adForm.condition = this.user.about_me
      } else {
        this.adForm.condition = ''
      }
    }
  },
  computed: {
    ...mapGetters({
      user: 'user',
      currencyPrice: 'currencyPrice',
      currencyFullData: 'currencyFullData'
    }),
    currencyPriceC(){
      this.actualPrice  = this.currencyPrice
      return this.actualPrice
    },
    returnCurrency(){
      switch(this.currencyFullData.type){
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
    equation() {
      let currencyName = this.currencyOptions.find(currency => {
        return currency.value === this.adForm.currency
      })
      return `usdt_in_${currencyName.name.toLowerCase()}*${this.adForm.profit}`
    },
    yourVersion() {
      return this.adForm.payment_method === 4;
    },
    inputHeader() {
      return this.adForm.type === 2 ? this.$t('bid.wantToSell') : this.$t('bid.wantToBuy')
    }
  },
  methods: {
    resetProfit(){
      this.adForm.profit = 0
    },
    defaultRate(){
      this.adForm.profit = 0
      this.actualPrice = this.currencyPrice
    },
    keyPressBackspace(){
      this.adForm.profit = 0
      this.actualPrice = this.currencyPrice
    },
    editTokenPrice(){
      this.actualPrice =  this.currencyPrice + (+this.adForm.profit * this.currencyPrice / 100)
    },
    async createAd(save = false) {
      if (this.adForm.fixed_price) {
        if (isNaN(Number(this.adForm.price)) || Number(this.adForm.price) <= 0) {
          this.$toast.showMessage({
            content: this.$t('bid.correctPrice'),
            red: true
          })
          return
        }
      }

      if (!this.adForm.amount_usdt || this.adForm.amount_usdt <= 0) {
        this.$toast.showMessage({
          content: this.$t('bid.quantity'),
          red: true
        })
      } else if (!this.adForm.bot_limit || !this.adForm.top_limit) {
        this.$toast.showMessage({
          content: this.$t('bid.limits'),
          red: true
        })
      } else if (!this.adForm.condition) {
        this.$toast.showMessage({
          content: this.$t('bid.terms'),
          red: true
        })
      } else {
        let res

        if (save) {
          res = await this.$store.dispatch('order/updateOrder', { id: this.$route.query.edit, data: this.adForm })
          if (res) {
            this.$toast.showMessage({
              content: this.$t('bid.adSaved'),
              green: true
            })

            this.$nuxt.context.redirect(`/order/${this.$route.query.edit}`)
          }
        } else {
          if(this.adForm.bank_title){
            this.adForm.other_payment_method = this.adForm.bank_title
          }
          res = await this.$store.dispatch('order/createOrder', this.adForm)
          if (res) {
            this.showModal = true
          }
        }
      }
    },
    toggleModal(state) {
      this.showModal = state
    }
  },
  async asyncData({ store, query }) {
    let adForm = {
      type: 1,
      bot_limit: null,
      top_limit: null,
      amount_usdt: null,
      payment_method: 1,
      bank_title: '',
      currency: 1,
      condition: '',
      profit: 0,
      fixed_price: false,
      price: 0
    }

    await store.dispatch('fetchCurrencyPrice' , adForm.currency)

    let res = null
     // default adForm

    // Если в URL есть параметр edit, выполнить запрос на /order/<id>, заполнить дефолтный adform выше и вернуть
    if (query.hasOwnProperty('edit')) {
      if (query.edit.length > 0) {
        res = await store.$axios.get(`/order/${query.edit}`)

        for (const key in adForm) {
          adForm[key] = res.data[key]
        }

        let profitMode = 'formula'

        if (adForm.fixed_price) {
          profitMode = 'fixed'
        }

        return {
          profitMode,
          editMode: true,
          adForm
        }
      }
    }

    return {
      adForm
    }
  },
  created(){
    console.log(this.adForm.price);
    this.actualPrice = this.adForm ? this.adForm.price : this.currencyPrice
  },
  mounted(){
  }
}
</script>

<style lang="scss">
.create-order-price{
  margin-bottom: 20px;
  font-size: 30px;
}

</style>
