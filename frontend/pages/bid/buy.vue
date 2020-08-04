<template lang="pug">
  div.create-ad
    p.create-ad__token-price Текущий курс токена 
      span.green 77,44 
      span ₽/USDT
    header.create-ad__navigation
      h1 Купить USDT
      nuxt-link(class="create-ad__link" to="/bid/sell/") Продать USDT
    hr
    div.create-ad__form
      Input.create-ad__input(v-model="adForm.bank_title" header="Название банка" placeholder="Банк")
      Input.create-ad__input(v-model="adForm.amount_usdt" type="number" header="Сколько Вы хотите купить" placeholder="0" endIcon="usdt")
      Input.create-ad__input(v-model="adForm.profit" header="Прибыль" placeholder="Прибыль" type="number" endIcon="procent" hint)
      Input.create-ad__input(v-model="adForm.profit" header="Уравнение установление цены" placeholder="" type="text")
      div.create-ad__gap
        Input.mr-30(v-model="adForm.bot_limit" :width="150" type="number" header="Минимальный лимит транзакции")
        Input(v-model="adForm.top_limit" :width="150" type="number" header="Максимальный лимит транзакции")
      Textarea.create-ad__conditions(v-model="adForm.condition" placeholder="Напишите условия сделки")
      Checkbox(label="Вставить условия сделки из профиля")
      Button.create-ad__action(green @click.native="createAd") создать объявление
</template>

<script>
import Input from '~/components/app/Input'
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
import Checkbox from '~/components/app/Checkbox'
export default {
  components: { Input, Textarea, Button, Checkbox },
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
        condition: '',
        profit: 0
      }
    }
  },
  methods: {
    createAd() {
      this.$store.dispatch('ads/createAd', this.adForm)
    }
  }
}
</script>

<style lang="scss">

</style>
