<template>
  <section class="auth-form">
    <header class="auth-form__header">
      <h1 class="auth-form__title">
        {{$t('signup.reg')}}
      </h1>
      <nuxt-link class="auth-form__subtitle" to="/login">
        {{$t('signup.signin')}}
      </nuxt-link>
    </header>
    <ValidationObserver v-slot="{ invalid }">
      <form class="auth-form__form" autocomplete="off">
        <ValidationProvider
          tag="div"
          rules="required|userLength|user__"
          v-slot="{ errors }"
        >
          <Input
            v-model="registerForm.username"
            :placeholder="$t('signup.username')"
            icon="user"
            type="text"
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
            :placeholder="$t('signup.email')"
            icon="email"
            type="email"
          />
          <span class="error">{{ errors[0] }}</span>
        </ValidationProvider>
        <ValidationProvider
          tag="div"
          rules="required|pwdLength|pwdLowChar|pwdUpChar|pwdDigit|confirmed:confirmation"
          v-slot="{ errors }">
          <Input
            v-model="registerForm.password"
            :placeholder="$t('signup.pass')"
            icon="password"
            type="password"
          />
          <span class="error" v-html="errors[0]"></span>
        </ValidationProvider>
        <ValidationProvider
          tag="div"
          rules="required|pwdLength|pwdLowChar|pwdUpChar|pwdDigit" vid="confirmation"
          v-slot="{ errors }">
          <Input
            v-model="registerForm.repeat_password"
            :placeholder="$t('signup.passApprove')"
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
            :placeholder="$t('signup.ref')"
            icon="copy-green"
            type="text"
          />
          <span class="error">{{ errors[0] }}</span>
        </ValidationProvider>
      </form>
      <div class="auth-form__action">
        <Button
          @click.native="signUp"
          :disabled="invalid"
          green
        >
          {{$t('signup.signUp')}}
        </Button>
      </div>
    </ValidationObserver>
    <nuxt-link
      to="/forgot"
      class="auth-form__forgot-password"
    >
      {{$t('signup.remindPass')}}
    </nuxt-link>
  </section>
</template>

<script>
import Input from '~/components/app/Input'
import Button from '~/components/app/Button'
import { ValidationObserver, ValidationProvider } from 'vee-validate'
import { mapGetters } from 'vuex'

export default {
  middleware: ['notAuthRequired'],
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
  computed: {
    referralId() {
      const { query } = this.$route
      return query.ref ? query.ref : ''
    },
    ...mapGetters({
      localeId: 'i18n/GET_LOCALE_ID'
    })
  },
  methods: {
    signUp() {
      let preparedForm = this.registerForm

      if (this.referralId) {
        preparedForm.referral_id = this.referralId
      }
      this.$store.dispatch('signUp', { ...preparedForm, language: this.localeId })
    }
  }
}
</script>

<style lang="scss"></style>
