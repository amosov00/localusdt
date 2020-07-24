<template lang="pug">
	section.signup
		header.signup__header
			h1.signup__title Регистрация
			nuxt-link.signup__subtitle(to="/login") Вход
		form.signup__form
			Input(v-model="registerForm.userName" placeholder="Имя пользователя" icon="user" type="text")
			Input(v-model="registerForm.email" placeholder="Эл. почта" icon="email" type="email")
			Input(v-model="registerForm.password" placeholder="Пароль" icon="password" type="password")
			Input(v-model="registerForm.passwordRepeat" placeholder="Подтверждение пароля" icon="password" type="password")
		div.signup__action
			Button(green @click.native="signUp") Зарегистрироваться
		p.signup__terms Нажимая “зарегистрироваться”, я принимаю 
			nuxt-link.signup__link(to="/") политику в отношении персональных данных 
			span и 
			nuxt-link.signup__link(to="/") пользовательское соглашение 
</template>

<script>
import Input from "~/components/app/Input";
import Button from "~/components/app/Button";
export default {
	components: { Input, Button },
	data() {
		return {
			registerForm: {
        userName: '',
        email: '',
        password: '',
        passwordRepeat: ''
			}
		}
	},
	methods: {
		async signUp() {
			await this.$store.dispatch("signUp", this.registerForm);
		}
	}
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

	&__form {
		& > * {
			margin-bottom: 20px;
		}
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
