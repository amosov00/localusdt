<template>
	<section class="auth-form">
		<header class="auth-form__header">
			<h1 class="auth-form__title">{{$t('signup.signin')}}</h1>
			<nuxt-link class="auth-form__subtitle" to="/signup">
				{{$t('signup.reg')}}
			</nuxt-link>
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
						:placeholder="$t('signup.email')"
						icon="email"
						type="email"
					/>
					<span class="error">{{ errors[0] }}</span>
				</ValidationProvider>
				<ValidationProvider rules="required" v-slot="{ errors }">
					<Input
						v-model="loginForm.password"
						:placeholder="$t('signup.pass')"
						icon="password"
						type="password"
					/>
					<span class="error">{{ errors[0] }}</span>
				</ValidationProvider>
			</form>
			<div class="auth-form__action">
				<Button @click.native="login" :disabled="invalid" green>{{$t('signup.signin2')}}</Button>
			</div>
		</ValidationObserver>
		<nuxt-link to="/forgot" class="auth-form__forgot-password">
			{{$t('signup.remindPass')}}
		</nuxt-link>
	</section>
</template>

<script>
import Input from '~/components/app/Input'
import Button from '~/components/app/Button'
import { ValidationObserver, ValidationProvider } from 'vee-validate'
import { mapGetters } from 'vuex';
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
