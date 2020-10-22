<template lang="pug">
  div.create-order
    p.create-order__token-price {{$t('bid.actualCourse')}}
      =' '
      span.green {{commaSplitting(currencyPrice)}}
      span ₽/USDT
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
        :header="$t('bid.payType')"
        )
        Select(
        :options="currencyOptions"
        v-model="adForm.currency"
        :width="80"
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
      div.radio-group
        label(for="profit-is-formula")
          input(id="profit-is-formula"
          type="radio"
          value="formula"
          name="profit-mode"
          v-model="profitMode")
          span {{$t('bid.formula')}}
        label(for="profit-is-fixed")
          input(
          id="profit-is-fixed"
          type="radio"
          value="fixed"
          name="profit-mode"
          v-model="profitMode")
          span {{$t('bid.fixed')}}
      Input.create-order__input(
      v-model="adForm.price"
      :header="$t('bid.price')"
      :placeholder="$t('bid.price')"
      v-if="adForm.fixed_price")

      Input.create-order__input(
      v-model="adForm.profit"
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
      placeholder=""
      type="text"
      v-if="profitMode === 'formula'")

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
        //- Select.create-order__gap--select(:options="currencyOptions" v-model="adForm.currency" :width="80")
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
        { name: 'RUB', value: 1 }
        // { name: 'USD', value: 2 },
        // { name: 'EUR', value: 3 }
      ],
      paymentOptions: [
        { name: this.$t('main.sberTransfer'), value: 1 },
        { name: this.$t('main.tinkofTransfer'), value: 2 },
        { name: this.$t('main.otherWay'), value: 3 }
      ],
      showModal: false,
      checkbox: false
    }
  },
  watch: {
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
      currencyPrice: 'currencyPrice'
    }),
    equation() {
      let currencyName = this.currencyOptions.find(currency => {
        return currency.value === this.adForm.currency
      })
      return `usdt_in_${currencyName.name.toLowerCase()}*${this.adForm.profit}`
    },
    yourVersion() {
      return this.adForm.payment_method === 3;
    },
    inputHeader() {
      return this.adForm.type === 2 ? this.$t('bid.wantToSell') : this.$t('bid.wantToBuy')
    }
  },
  methods: {
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

    await store.dispatch('fetchCurrencyPrice')

    let res = null
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
    } // default adForm

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
  }
}
</script>

<style lang="scss"></style>
