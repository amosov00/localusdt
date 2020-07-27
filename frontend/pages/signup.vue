<template lang="pug">
	section.auth-form
		header.auth-form__header
			h1.auth-form__title Регистрация
			nuxt-link.auth-form__subtitle(to="/login") Вход
		form.auth-form__form
			Input(v-model="registerForm.username" placeholder="Имя пользователя" icon="user" type="text")
			Input(v-model="registerForm.email" placeholder="Эл. почта" icon="email" type="email")
			Input(v-model="registerForm.password" placeholder="Пароль" icon="password" type="password")
			Input(v-model="registerForm.repeat_password" placeholder="Подтверждение пароля" icon="password" type="password")
		div.auth-form__action
			Button(green @click.native="signUp") Зарегистрироваться
		p.auth-form__terms Нажимая “зарегистрироваться”, я принимаю 
			nuxt-link.auth-form__link(to="/") политику в отношении персональных данных 
			span и 
			nuxt-link.auth-form__link(to="/") пользовательское соглашение 
</template>

<script>
import Input from '~/components/app/Input'
import Button from '~/components/app/Button'
export default {
  components: { Input, Button },
  data() {
    return {
      registerForm: {
        username: '',
        email: '',
        password: '',
        repeat_password: ''
      }
    }
  },
  methods: {
    signUp() {
      this.$store.dispatch('signUp', this.registerForm)
    }
  }
}
</script>

<style lang="scss"></style>
