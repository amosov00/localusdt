<template lang="pug">
	section.auth-form
		header.auth-form__header
			h1.auth-form__title Вход
			nuxt-link.auth-form__subtitle(to="/signup") Регистрация
		form.auth-form__form
			Input(v-model="loginForm.email" placeholder="Эл. почта" icon="email" type="email")
			Input(v-model="loginForm.password" placeholder="Пароль" icon="password" type="password")
		div.auth-form__action
			Button(@click.native="login" green) Войти
		nuxt-link.auth-form__forgot-password(to="/forgot") Забыли пароль?
</template>

<script>
import Input from '~/components/app/Input'
import Button from '~/components/app/Button'
export default {
  name: 'login',
  components: { Input, Button },
  data() {
    return {
      loginForm: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    login() {
      this.$store.dispatch('logIn', this.loginForm)
    }
  }
}
</script>

<style lang="scss"></style>
