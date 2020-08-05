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
      Select(:options="options" :selected="selected")
      Input.create-order__input(v-model="adForm.bank_title" header="Название банка" placeholder="Банк")
      Input.create-order__input(v-model="adForm.amount_usdt" type="number" header="Сколько Вы хотите купить" placeholder="0" endIcon="usdt")
      Input.create-order__input(v-model="adForm.profit" header="Прибыль" placeholder="Прибыль" type="number" endIcon="procent" hint)
      Input.create-order__input(v-model="adForm.profit" header="Уравнение установление цены" placeholder="" type="text")
      div.create-order__gap
        Input.mr-30(v-model="adForm.bot_limit" :width="150" type="number" header="Минимальный лимит транзакции")
        Input(v-model="adForm.top_limit" :width="150" type="number" header="Максимальный лимит транзакции")
      Textarea.create-order__conditions(v-model="adForm.condition" placeholder="Напишите условия сделки")
      Checkbox(label="Вставить условия сделки из профиля")
      Button.create-order__action(green @click.native="createAd") создать объявление
</template>

<script>
import Input from '~/components/app/Input'
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
import Checkbox from '~/components/app/Checkbox'
import Select from '~/components/app/Select'
export default {
  components: { Input, Textarea, Button, Checkbox, Select },
  middleware: ['authRequired'],
  data() {
    return {
      adForm: {
        type: 1,
        bot_limit: 0,
        top_limit: 0,
        amount_usdt: 0,
        payment_method: 1,
        bank_title: 'Сбербанк',
        currency: 1,
        condition: 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor.  Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes,nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.',
        profit: 0
      },
      options: [
        { name: 'RUB', value: 'rub' },
        { name: 'USD', value: 'usd' },
        { name: 'EUR', value: 'eur' }
      ],
      selected: 'Selected'
    }
  },
  methods: {
    createAd() {
      this.$store.dispatch('order/createOrder', this.adForm)
    }
  }
}
</script>

<style lang="scss">

</style>
