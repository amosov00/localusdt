<template lang="pug">
  div.create-order
    p.create-order__token-price Текущий курс токена
      span.green {{commaSplitting(currencyPrice)}}
      span ₽/USDT
    header.create-order__navigation
      h1 Продать USDT
    hr
    div.create-order__form
      div.create-order__options
        Select(:options="paymentOptions" v-model="adForm.payment_method" :width="350" header="Способ оплаты")
        Select(:options="currencyOptions" v-model="adForm.currency" :width="80" header="Валюты" hideArrow)
      Input.create-order__input( v-if="yourVersion" v-model="adForm.bank_title" header="" placeholder="Свой вариант")
      Input.create-order__input.mt-40.mb-80(v-model="adForm.amount_usdt" type="number" :header="inputHeader" placeholder="0" endIcon="usdt")
      div.radio-group
        label(for="profit-is-formula")
          input(id="profit-is-formula" type="radio" value="formula" name="profit-mode" v-model="profitMode")
          span Формула
        label(for="profit-is-fixed")
          input(id="profit-is-fixed" type="radio" value="fixed" name="profit-mode" v-model="profitMode")
          span Фиксированная
      Input.create-order__input(v-model="adForm.price" header="Цена" placeholder="Цена" v-if="adForm.fixed_price")
      Input.create-order__input(v-model="adForm.profit" header="Прибыль" placeholder="Прибыль" type="number" endIcon="procent" hint)
      Input.create-order__input(disabled :value="equation" header="Уравнение установление цены" placeholder="" type="text")
      div.create-order__gap
        Input.mr-30(v-model="adForm.bot_limit" :width="250" type="number" header="Минимальный лимит транзакции")
        Input(v-model="adForm.top_limit" :width="250" type="number" header="Максимальный лимит транзакции")
        //- Select.create-order__gap--select(:options="currencyOptions" v-model="adForm.currency" :width="80")
      Textarea.create-order__conditions(v-model="adForm.condition" placeholder="Напишите условия сделки")
      Checkbox(v-model="checkbox" label="Вставить условия сделки из профиля")
      Button.create-order__action(green @click.native="createAd") создать объявление
      Modal(:show="showModal" @toggleModal="toggleModal($event)" :type="2")
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
      profitMode: 'formula',
      adForm: {
        type: 2,
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
        { name: 'Банковский перевод: Сбербанк', value: 1 },
        { name: 'Банковский перевод: Тиньков', value: 2 },
        { name: 'Свой вариант', value: 3 }
      ],
      showModal: false,
      checkbox: false
    }
  },
  watch: {
    profitMode() {
      if(this.profitMode === 'fixed') {
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

      if(this.profitMode === 'fixed') {
        return `${this.currencyPrice.toFixed(2)}*${this.adForm.profit}`
      }

      return `usdt_in_${currencyName.name.toLowerCase()}*${this.adForm.profit}`
    },
    yourVersion() {
      if (this.adForm.payment_method === 3) {
        return true
      }
      return false
    },
    inputHeader() {
      if (this.adForm.type === 2) {
        return 'Сколько вы хотите продать'
      } else {
        return 'Сколько вы хотите купить'
      }
    }
  },
  methods: {
    async createAd() {
      if(this.adForm.fixed_price) {
        if(isNaN(Number(this.adForm.price)) || Number(this.adForm.price) <= 0) {
          this.$toast.showMessage({
            content: 'Введите корректную цену',
            red: true
          })
          return
        }
      }

      if (!this.adForm.amount_usdt || this.adForm.amount_usdt <= 0) {
        this.$toast.showMessage({
          content: 'Введите количество USDT',
          red: true
        })
      } else if (!this.adForm.bot_limit || !this.adForm.top_limit) {
        this.$toast.showMessage({
          content: 'Введите лимиты объявления',
          red: true
        })
      } else if (!this.adForm.condition) {
        this.$toast.showMessage({
          content: 'Введите условие',
          red: true
        })
      } else {
        const res = await this.$store.dispatch('order/createOrder', this.adForm)
        if (res) {
          this.showModal = true
        }
      }
    },
    toggleModal(state) {
      this.showModal = state
    }
  },
  asyncData({ store }) {
    return store.dispatch('fetchCurrencyPrice')
  }
}
</script>

<style lang="scss" scoped>
  .radio-group {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 40px;

    label {
      margin-right: 20px;
      cursor: pointer;

      &:hover {
        opacity: 0.8;
      }

      &:last-child {
        margin-right: 0;
      }
    }
    span {
      margin-left: 5px;
    }
  }
</style>
