<template>
  <section class="auth-form">
    <header class="auth-form__header">
      <h1 class="auth-form__title">Изменить пароль</h1>
    </header>
    <ValidationObserver v-slot="{ invalid }">
      <form class="auth-form__form">
        <ValidationProvider
          tag="div"
          rules="required|min:8|upCase|number"
          v-slot="{ errors }"
        >
          <Input
            v-model="changeForm.old_password"
            placeholder="Старый пароль"
            type="password"
            icon="password"
          />
          <span class="error">{{ errors[0] }}</span>
        </ValidationProvider>
        <ValidationProvider
          tag="div"
          rules="required|min:8|confirmed:confirmation|upCase|number"
          v-slot="{ errors }"
        >
          <Input
            v-model="changeForm.password"
            placeholder="Новый пароль"
            type="password"
            icon="password"
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
            v-model="changeForm.repeat_password"
            placeholder="Подтверждение пароля"
            type="password"
            icon="password"
          />
          <span class="error">{{ errors[0] }}</span>
        </ValidationProvider>
      </form>
      <div class="auth-form__action">
        <Button @click.native="change" :disabled="invalid" green
          >Сменить пароль</Button
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
