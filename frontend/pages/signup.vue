<template>
	<section class="auth-form">
		<header class="auth-form__header">
			<h1 class="auth-form__title">Регистрация</h1>
			<nuxt-link class="auth-form__subtitle" to="/login"
				>Вход</nuxt-link
			>
		</header>
		<ValidationObserver v-slot="{ invalid }">
			<form class="auth-form__form">
				<Input
					v-model="registerForm.username" placeholder="Имя пользователя" icon="user" type="text"
				/>
					<ValidationProvider
				tag="div"
				rules="required|email"
				v-slot="{ errors }"
				>
					<Input
						v-model="registerForm.email"
						placeholder="Эл. почта"
						icon="email"
						type="email"
					/>
					<span class="error">{{ errors[0] }}</span>
				</ValidationProvider>
				<ValidationProvider tag="div" rules="required|min:8|upCase|lowCase|number|confirmed:confirmation"  v-slot="{ errors }">
					<Input
						v-model="registerForm.password"
						placeholder="Пароль"
						icon="password"
						type="password"
					/>
					<span class="error">{{ errors[0] }}</span>
				</ValidationProvider>
				<ValidationProvider tag="div"  rules="required|min:8|upCase|lowCase|number" vid="confirmation" v-slot="{ errors }">
					<Input
						v-model="registerForm.repeat_password"
						placeholder="Пароль"
						icon="password"
						type="password"
					/>
					<span class="error">{{ errors[0] }}</span>
				</ValidationProvider>
			</form>
			<div class="auth-form__action">
				<Button@click.native="signUp" :disabled="invalid" green>Зарегистрироваться</Button>
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
	components: { Input, Button, ValidationObserver, ValidationProvider },
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
