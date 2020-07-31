<template lang="pug">
  div.bid
    p.bid__token-price Текущий курс токена 
      span.green 77,44 
      span ₽/USDT
    header.bid__navigation
      h1 Продать USDT
      nuxt-link(class="bid__link" to="/bid/sell/") Купить USDT
    hr
    div.bid__form
      Input.bid__input(v-model="adForm.bank_title" header="Название банка" placeholder="Банк")
      div.bid__input--hint
        Input.bid__input(v-model="adForm.profit" header="Прибыль" placeholder="Прибыль" type="number" endIcon="%" :width="475")
        p.paragraph-1 Размер прибыли, которую Вы хотите получить сверху рыночной цены.
      //- Input.bid__input(header="Уравнение установление цены" placeholder="Уравнение")
      div.bid__gap
        Input(v-model="adForm.bot_limit" :width="200" endIcon="RUB" type="number" header="Минимальный лимит транзакции")
        Input(v-model="adForm.top_limit" :width="200" endIcon="RUB" type="number" header="Максимальный лимит транзакции")
      Textarea.bid__conditions(v-model="adForm.condition" placeholder="Напишите условия сделки")
      Button.bid__action(green @click.native="createAd") создать объявление
</template>

<script>
import Input from '~/components/app/Input'
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
export default {
  components: { Input, Textarea, Button },
  middleware: ['authRequired'],
  data() {
    return {
      adForm: {
        bank_title: '',
        profit: 1,
        bot_limit: 0,
        top_limit: 0,
        condition: '',
        amount_usdt: 0,
        type: 1
      }
    }
  },
  methods: {
    createAd() {
      this.$store.dispatch('ads/createAd', this.adForm)
    }
  },
}
</script>

<style lang="scss">
.bid {
  margin-top: 30px;
  &__token-price {
    font-size: 14px;
    opacity: 0.7;
  }

  &__navigation {
    margin-top: 50px;
    margin-bottom: 10px;
  }

  &__link {
    @include montserrat
    display: inline-block;
    margin-top: 8px;
    font-size: 20px;
    opacity: .5;
    text-decoration: underline;
  }

  &__form {
    margin-top: 50px;
    width: 475px;
  }

  &__input {
    margin-bottom: 30px;

    &--hint {
      display: flex;
      width: 1080px;

      p {
        margin-left: 60px;
      }
    }
  }

  &__gap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 100px;
  }

  &__conditions {
    margin-top: 100px;
    margin-bottom: 60px;
  }

  &__action {
    margin-bottom: 50px;
  }
}
</style>
