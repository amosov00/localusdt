<template>
  <section class="auth-form">
    <header class="auth-form__header">
      <h1 class="auth-form__title">Изменить пароль</h1>
    </header>
    <form class="auth-form__form">
      <Input
        v-model="changeForm.old_password"
        placeholder="Старый пароль"
        type="password"
        icon="password"
      />
      <Input
        v-model="changeForm.password"
        placeholder="Новый пароль"
        type="password"
        icon="password"
      />
      <Input
        v-model="changeForm.repeat_password"
        placeholder="Подтверждение пароля"
        type="password"
        icon="password"
      />
    </form>
    <div class="auth-form__action">
      <Button @click.native="change" green>Сменить пароль</Button>
    </div>
  </section>
</template>

<script>
import Input from '~/components/app/Input'
import Button from '~/components/app/Button'
export default {
  name: 'change',
  components: {
    Input,
    Button
  },
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
