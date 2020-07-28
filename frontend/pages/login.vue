<template>
	<section class="auth-form">
		<header class="auth-form__header">
			<h1 class="auth-form__title">Вход</h1>
			<nuxt-link class="auth-form__subtitle" to="/signup"
				>Регистрация</nuxt-link
			>
		</header>
		<ValidationObserver v-slot="{ invalid }">
			<form class="auth-form__form">
				<ValidationProvider
					tag="div"
					rules="required|email"
					v-slot="{ errors }"
				>
					<Input
						v-model="loginForm.email"
						placeholder="Эл. почта"
						icon="email"
						type="email"
					/>
					<span class="error">{{ errors[0] }}</span>
				</ValidationProvider>
				<ValidationProvider rules="required|min:8|upCase|lowCase|number" v-slot="{ errors }">
					<Input
						v-model="loginForm.password"
						placeholder="Пароль"
						icon="password"
						type="password"
					/>
					<span class="error">{{ errors[0] }}</span>
				</ValidationProvider>
			</form>
			<div class="auth-form__action">
				<Button@click.native="login" :disabled="invalid" green>Войти</Button>
			</div>
		</ValidationObserver>
		<nuxt-link to="/forgot" class="auth-form__forgot-password"
			>Забыли пароль?</nuxt-link
		>
	</section>
</template>

<script>
import Input from '~/components/app/Input'
import Button from '~/components/app/Button'
import { ValidationObserver, ValidationProvider } from 'vee-validate'
export default {
  name: 'login',
  components: { Input, Button, ValidationObserver, ValidationProvider },
  data() {
    return {
      loginForm: {
        email: '',
        password: '',
      },
    }
  },
  methods: {
    login() {
      this.$store.dispatch('logIn', this.loginForm)
    },
  },
}
</script>

<style lang="scss">
</style>
