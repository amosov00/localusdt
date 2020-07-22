<template lang="pug">
  div.login
    header.login__header
      h1.login__title Вход
      nuxt-link.login__subtitle(to="/signup") Регистрация
    main.login__inputs
      Input(placeholder="Эл. почта" icon="email" type="email")
      Input(placeholder="Пароль" icon="password" type="password")
    div.login__action
      Button(green) Войти
    nuxt-link.login__forgot-password(to="/") Забыли пароль?
</template>

<script>
import Input from '~/components/app/Input'
import Button from '~/components/app/Button'
export default {
  components: { Input, Button }
}
</script>

<style lang="scss">
.login {
  width: 390px;
  margin: auto;
  padding-top: 100px;

  &__header {
    margin-bottom: 60px;
  }

  &__title {
    margin-bottom: 8px;
  }

  &__subtitle {
    @include montserrat;
    @include reset-link;
    text-decoration-line: underline;
    opacity: 0.5;
  }

  &__inputs {
    height: 110px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  &__action {
    margin-top: 50px;
    margin-bottom: 20px;
  }

  &__forgot-password {
    text-decoration: underline;
    color: $orange;
  }
}
</style>
