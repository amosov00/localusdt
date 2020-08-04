<template>
  <form>
    <h2 v-if="ad.type === 1">Сколько Вы хотите продать?</h2>
      <h2 v-else>Сколько Вы хотите купить?</h2>
      <div  v-if="$userIsLoggedIn()">
        <Input
          v-model="invoiceForm.amount_usdt"
          type="number"
          :width="150"
          placeholder="0,00"
        />
        <Textarea class="mt-10"
          placeholder="Напишите трейдеру сообщение с контактной или другой информацией 
(необязательно)"
        />
        <Button class="mt-20" green @click.native="createInvoice"
          >Отправить запрос на сделку</Button
        >
      </div>
      <nuxt-link v-else to="/signup">
        <Button orange>Зарегистрируйтесь бесплатно</Button>
      </nuxt-link>
  </form>
</template>

<script>
import Button from '~/components/app/Button'
import Input from '~/components/app/Input'
import Textarea from '~/components/app/Textarea'
export default {
  props: {
    ad: Object
  },
  components: {
    Button,
    Input,
    Textarea
  },
  data() {
    return {
      invoiceForm: {
        ads_id: this.$route.params.id,
        amount_usdt: 0
      }
    }
  },
  methods: {
    createInvoice() {
      if (this.invoiceForm.amount_usdt) {
        this.$store.dispatch('invoice/createInvoice', this.invoiceForm)
      } else {
        this.$toast.showMessage({ content: 'Введите сумму', red: true })
      }
    }
  },
}
</script>

<style lang="scss">

</style>