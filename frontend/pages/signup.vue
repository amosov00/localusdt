<template>
  <section class="auth-form">
    <header class="auth-form__header">
      <h1 class="auth-form__title">Регистрация</h1>
      <nuxt-link class="auth-form__subtitle" to="/login"
      >Вход
      </nuxt-link
      >
    </header>
    <ValidationObserver v-slot="{ invalid }">
      <form class="auth-form__form" autocomplete="off">
        <ValidationProvider
          tag="div"
          rules="required|userLength|user__"
          v-slot="{ errors }"
        >
          <Input
            v-model="registerForm.username" placeholder="Имя пользователя" icon="user" type="text"
          />
          <span class="error" v-html="errors[0]"></span>
        </ValidationProvider>
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
        <ValidationProvider tag="div" rules="required|pwdLength|pwdLowChar|pwdUpChar|pwdDigit|confirmed:confirmation"
                            v-slot="{ errors }">
          <Input
            v-model="registerForm.password"
            placeholder="Пароль"
            icon="password"
            type="password"
          />
          <span class="error" v-html="errors[0]"></span>
        </ValidationProvider>
        <ValidationProvider tag="div" rules="required|pwdLength|pwdLowChar|pwdUpChar|pwdDigit" vid="confirmation"
                            v-slot="{ errors }">
          <Input
            v-model="registerForm.repeat_password"
            placeholder="Подтверждение пароля"
            icon="password"
            type="password"
          />
          <span class="error" v-html="errors[0]"></span>
        </ValidationProvider>
        <ValidationProvider
          tag="div"
          v-slot="{ errors }"
        >
          <Input
            :value="referralId"
            placeholder="Реферальный код"
            icon="copy-green"
            type="text"
          />
          <span class="error">{{ errors[0] }}</span>
        </ValidationProvider>
      </form>
      <div class="auth-form__action">
        <Button @click.native="signUp" :disabled="invalid" green>Зарегистрироваться</Button>
      </div>
    </ValidationObserver>
    <nuxt-link to="/forgot" class="auth-form__forgot-password"
    >Забыли пароль?
    </nuxt-link
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
  computed:{
    referralId() {
      const {query} = this.$route
      return query.ref ? query.ref : ''
    }
  },
  methods: {
    signUp() {
      let preparedForm = this.registerForm
      if(this.referralId) {
        preparedForm.referral_id = this.referralId
      }
      this.$store.dispatch('signUp', preparedForm)
    }
  }
}
</script>

<style lang="scss"></style>
