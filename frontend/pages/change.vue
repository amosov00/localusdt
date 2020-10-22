<template>
  <section class="auth-form">
    <header class="auth-form__header">
      <h1 class="auth-form__title">{{$t('signup.changePass')}}</h1>
    </header>
    <ValidationObserver v-slot="{ invalid }">
      <form class="auth-form__form">
        <ValidationProvider
          tag="div"
          rules="required|pwdContain|pwdLength|pwdLowChar|pwdUpChar|pwdDigit"
          v-slot="{ errors }"
        >
          <Input
            v-model="changeForm.old_password"
            :placeholder="$t('signup.oldPass')"
            type="password"
            icon="password"
          />
          <span class="error" v-html="errors[0]"></span>
        </ValidationProvider>
        <ValidationProvider
          tag="div"
          rules="required|pwdContain|pwdLength|pwdLowChar|pwdUpChar|pwdDigit|confirmed:confirmation"
          v-slot="{ errors }"
        >
          <Input
            v-model="changeForm.password"
            :placeholder="$t('signup.newPass')"
            type="password"
            icon="password"
          />
          <span class="error" v-html="errors[0]"></span>
        </ValidationProvider>
        <ValidationProvider
          tag="div"
          rules="required|pwdContain|pwdLength|pwdLowChar|pwdUpChar|pwdDigit"
          vid="confirmation"
          v-slot="{ errors }"
        >
          <Input
            v-model="changeForm.repeat_password"
            :placeholder="$t('signup.passApprove')"
            type="password"
            icon="password"
          />
          <span class="error" v-html="errors[0]"></span>
        </ValidationProvider>
      </form>
      <div class="auth-form__action">
        <Button @click.native="change" :disabled="invalid" green
          >{{ $t('signup.changePass2') }}</Button
        >
      </div>
    </ValidationObserver>
  </section>
</template>

<script>
import Input from '~/components/app/Input'
import Button from '~/components/app/Button'
import { ValidationObserver, ValidationProvider } from 'vee-validate'
export default {
  name: 'change',
  components: { Input, Button, ValidationObserver, ValidationProvider },
  data() {
    return {
      changeForm: {
        old_password: '',
        password: '',
        repeat_password: ''
      }
    }
  },
  methods: {
    change() {
      this.$store.dispatch('changePassword', this.changeForm)
    }
  }
}
</script>

<style lang="scss"></style>
