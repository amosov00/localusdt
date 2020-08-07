<template lang="pug">
  div.create-order
    p.create-order__token-price Текущий курс токена 
      span.green 77,44 
      span ₽/USDT
    header.create-order__navigation
      h1 Купить USDT
      nuxt-link(class="create-order__link" to="/bid/sell/") Продать USDT
    hr
    div.create-order__form
      div.create-order__options
        Select(:options="paymentOptions" v-model="adForm.payment_method" :width="350" header="Способ оплаты")
        Select(:options="currencyOptions" v-model="adForm.currency" :width="80" header="Валюты")
      Input.create-order__input( v-if="yourVersion" v-model="adForm.bank_title" header="" placeholder="Свой вариант")
      Input.create-order__input.mb-110(v-model="adForm.amount_usdt" type="number" header="Сколько Вы хотите купить" placeholder="0" endIcon="usdt")
      Input.create-order__input(v-model="adForm.profit" header="Прибыль" placeholder="Прибыль" type="number" endIcon="procent" hint)
      Input.create-order__input(disabled :value="equation" header="Уравнение установление цены" placeholder="" type="text")
      div.create-order__gap
        Input.mr-30(v-model="adForm.bot_limit" :width="250" type="number" header="Минимальный лимит транзакции")
        Input(v-model="adForm.top_limit" :width="250" type="number" header="Максимальный лимит транзакции")
        //- Select.create-order__gap--select(:options="currencyOptions" v-model="adForm.currency" :width="80")
      Textarea.create-order__conditions(v-model="adForm.condition" placeholder="Напишите условия сделки")
      Checkbox(label="Вставить условия сделки из профиля")
      Button.create-order__action(green @click.native="createAd") создать объявление
      Modal(:show="showModal")
</template>

<script>
import Input from '~/components/app/Input'
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
import Checkbox from '~/components/app/Checkbox'
import Select from '~/components/app/Select'
import Modal from '~/components/app/Modal'
export default {
  components: { Input, Textarea, Button, Checkbox, Select, Modal },
  middleware: ['authRequired'],
  data() {
    return {
      adForm: {
        type: 1,
        bot_limit: 0,
        top_limit: 0,
        amount_usdt: 0,
        payment_method: 1,
        bank_title: '',
        currency: 1,
        condition: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor.  Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes,nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.',
        profit: 0
      },
      currencyOptions: [
        { name: 'RUB', value: 1 },
        { name: 'USD', value: 2 },
        { name: 'EUR', value: 3 }
      ],
      paymentOptions: [
        { name: 'Банковский перевод: Сбербанк', value: 1 },
        { name: 'Банковский перевод: Тиньков', value: 2 },
        { name: 'Свой вариант', value: 3 }
      ],
      showModal: false
    }
  },
  computed: {
    equation() {
      let currencyName = this.currencyOptions.find(currency => {
        return currency.value === this.adForm.currency
      })
      return `usdt_in_${currencyName.name.toLowerCase()}*${this.adForm.profit}`
    },
    yourVersion() {
      if(this.adForm.payment_method === 3) {
        return true
      }
      return false
    }
  },
  methods: {
    createAd() {
      this.showModal = true
      // this.$store.dispatch('order/createOrder', this.adForm)
    }
  }
}
</script>

<style lang="scss">

</style>
