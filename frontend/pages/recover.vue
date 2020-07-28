<template>
  <section class="auth-form">
    <header class="auth-form__header">
      <h1 class="auth-form__title">Восстановление пароля</h1>
    </header>
    <ValidationObserver v-slot="{ invalid }">
      <form class="auth-form__form">
        <ValidationProvider
          tag="div"
          rules="required|min:8|confirmed:confirmation|upCase|number"
          v-slot="{ errors }"
        >
          <Input
            v-model="recoverForm.password"
            placeholder="Новый пароль"
            icon="password"
            type="password"
          />
          <span class="error">{{ errors[0] }}</span>
        </ValidationProvider>
        <ValidationProvider
          tag="div"
          rules="required|min:8|upCase|number"
          vid="confirmation"
          v-slot="{ errors }"
        >
          <Input
            v-model="recoverForm.repeat_password"
            placeholder="Подтверждение пароля"
            icon="password"
            type="password"
          />
          <span class="error">{{ errors[0] }}</span>
        </ValidationProvider>
      </form>
      <div class="auth-form__action">
        <Button @click.native="recover" :disabled="invalid" green
          >Отправить</Button
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
  name: 'recover',
  components: { Input, Button, ValidationObserver, ValidationProvider },
  data() {
    return {
      recoverForm: {
        password: '',
        repeat_password: ''
      }
    }
  },
  methods: {
    recover() {
      const data = {
        password: this.recoverForm.password,
        repeat_password: this.recoverForm.repeat_password,
        recover_code: this.query.recover_code
      }

      this.$store.dispatch('finishRecover', data)
    }
  },
  asyncData({ query }) {
    return { query }
  }
}
</script>

<style lang="scss">
.recover {
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
