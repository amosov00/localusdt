<template lang="pug">
  div.bid
    p.bid__token-price Текущий курс токена 
      span.green 77,44 
      span ₽/USDT
    header.bid__navigation
      h1 Продать USDT
      nuxt-link(to="/bid/sell/") Купить USDT
    hr
    div.bid__form
      Input.bid__input(header="Название банка" placeholder="Банк")
      div.bid__input--hint
        Input.bid__input(header="Прибыль" placeholder="Прибыль" endIcon="%" :width="475")
        p.paragraph-1 Размер прибыли, которую Вы хотите получить сверху рыночной цены.
      Input.bid__input(header="Уравнение установление цены" placeholder="Уравнение")
      div.bid__gap
        Input(:width="200" endIcon="RUB" type="number" header="Минимальный лимит транзакции")
        Input(:width="200" endIcon="RUB" type="number" header="Минимальный лимит транзакции")
      Textarea.bid__conditions(placeholder="Напишите условия сделки")
      Button.bid__action(green) создать объявление
</template>

<script>
import Input from '~/components/UI/Input'
import Textarea from '~/components/UI/Textarea'
import Button from '~/components/UI/Button'
export default {
  components: { Input, Textarea, Button }
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
