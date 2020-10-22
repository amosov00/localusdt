<template>
  <form class="order-form">
    <h2 v-if="order.type === 2">{{ $t('orderForm.wantToBuy') }}</h2>
    <h2 v-else>{{ $t('orderForm.wantToSell') }}</h2>
    <div v-if="$userIsLoggedIn()">
      <Input
        v-model="invoiceForm.amount_usdt"
        type="number"
        :width="150"
        placeholder="0,00"
      />
      <Textarea
        class="mt-20"
        :placeholder="$t('orderForm.writeTo')"
      />
      <Button class="mt-20" green @click.native="createInvoice">
        {{ $t('orderForm.send') }}
      </Button>
    </div>
    <nuxt-link v-else to="/signup">
      <Button orange>
        {{ $t('orderForm.reg') }}
      </Button>
    </nuxt-link>
  </form>
</template>

<script>
import Button from '~/components/app/Button'
import Input from '~/components/app/Input'
import Textarea from '~/components/app/Textarea'
export default {
  props: {
    order: Object
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
        this.$toast.showMessage({ content: this.$t('orderForm.writeSum'), red: true })
      }
    }
  }
}
</script>

<style lang="scss">
.order-form {
  & > * {
    margin-bottom: 20px;
  }
}
</style>
