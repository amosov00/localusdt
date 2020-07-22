<template lang="pug">
  form.signup
    header.signup__header
      h1.signup__title Регистрация
      nuxt-link.signup__subtitle(to="/login") Вход
    main.signup__inputs
      Input(v-model="email" placeholder="Имя пользователя" icon="user" type="text")
      Input(placeholder="Эл. почта" icon="email" type="email")
      Input(placeholder="Пароль" icon="password" type="password")
    div.signup__action
      Button(green) Зарегистрироваться
    p.signup__terms Нажимая “зарегистрироваться”, я принимаю 
      nuxt-link.signup__link(to="/") политику в отношении персональных данных 
      span и 
      nuxt-link.signup__link(to="/")  пользовательское соглашение 
</template>

<script>
import Input from "~/components/app/Input";
import Button from "~/components/app/Button";
export default {
  components: { Input, Button },
  data() {
    return {
      email: ''
    }
  },
};
</script>

<style lang="scss">
.signup {
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
    height: 175px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  &__action {
    margin-top: 50px;
    margin-bottom: 20px;
  }

  &__terms {
  }

  &__link {
    @include reset-link;
    color: $orange !important;
  }
}
</style>
