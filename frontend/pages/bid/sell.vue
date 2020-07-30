<template lang="pug">
  div.bid
    p.bid__token-price Текущий курс токена 
      span.green 77,44 
      span ₽/USDT
    header.bid__navigation
      h1 Купить USDT
      nuxt-link(class="bid__link" to="/bid/buy/") Продать USDT
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
      Button.bid__action(green) создать объявление
</template>

<script>
import Input from '~/components/app/Input'
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
export default {
  name: 'bid-sell',
  components: { Input, Textarea, Button },
  data() {
    return {
      adForm: {
        bank_title: '',
        profit: 1,
        bot_limit: '',
        top_limit: '',
        condition: '',
        type: 2
      }
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
