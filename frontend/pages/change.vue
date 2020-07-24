<template>
	<section class="change">
    <header class="change__header">
      <h1 class="change__title">Изменить пароль</h1>
    </header>
		<form class="change__form">
			<Input v-model="changeForm.old_password" placeholder="Старый пароль" type="password" icon="password" />
			<Input v-model="changeForm.password" placeholder="Новый пароль" type="password" icon="password" />
			<Input v-model="changeForm.repeat_password" placeholder="Подтверждение пароля" type="password" icon="password" />
		</form>
    <div class="change__action">
      <Button @click.native="change" green >Сменить пароль</Button>
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
        repeat_password: '',
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

<style lang="scss">
.change {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding-top: 100px;

  &__title {
    margin-bottom: 20px;
  }

	&__form {
		width: 390px;
	  margin: auto;
    
    & > * {
			margin-bottom: 20px;
		}
	}
}
</style>
