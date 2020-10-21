<template>
  <section class="auth-form">
    <header class="auth-form__header">
      <h1 class="auth-form__title">{{ $t('signup.forgotPass') }}</h1>
    </header>
    <ValidationObserver v-slot="{ invalid }">
      <form class="auth-form__form">
        <ValidationProvider
          tag="div"
          rules="required|email"
          v-slot="{ errors }"
        >
          <Input
            v-model="forgotForm.email"
            :placeholder="$t('signup.email')"
            icon="email"
            type="email"
          />
          <span class="error">{{ errors[0] }}</span>
        </ValidationProvider>
      </form>
      <div class="auth-form__action">
        <Button @click.native="startRecover" :disabled="invalid" green
          >{{ $t('signup.send') }}</Button
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
  name: 'forgot',
  components: { Input, Button, ValidationObserver, ValidationProvider },
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
