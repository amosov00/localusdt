<template lang="pug">
	section.auth-form
		header.auth-form__header
			h1.auth-form__title Восстановление пароля
		form.auth-form__form
			Input(v-model="forgotForm.email" placeholder="Эл. почта" icon="email" type="email")
		div.auth-form__action
			Button(@click.native="startRecover" green) Отправить
</template>

<script>
import Input from '~/components/app/Input'
import Button from '~/components/app/Button'
export default {
  name: 'forgot',
  components: { Input, Button },
  data() {
    return {
      forgotForm: {
        email: ''
      }
    }
  },
  methods: {
    startRecover() {
      this.$store.dispatch('startRecover', this.forgotForm)
    }
  }
}
</script>

<style lang="scss">
.forgot {
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

  &__forgot-password {
    text-decoration: underline;
    color: $orange;
  }
}
</style>
