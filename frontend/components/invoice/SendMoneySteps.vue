<template>
  <div class="steps">
    <div class="step-1">
      <p>
        <span class="opacity-50">{{$t('sendMoney.step')}} 1: </span>
        {{$t('sendMoney.payToSeller')}}
      </p>
      <p>
        {{$t('sendMoney.text1', {msg: invoice.seller_username})}}
      </p>
      <div class="steps-list">
        <div class="steps-list__row">
          <p>
            <span class="opacity-50">{{$t('sendMoney.sum')}} </span>
          </p>
          <p class="steps-list--left">
            <span>{{ commaSplitting(invoice.amount) }} ₽</span>
          </p>
        </div>
        <div class="steps-list__row">
          <p>
            <span class="opacity-50">{{$t('sendMoney.payType')}} </span>
          </p>
          <p class="steps-list--left">
            <span>{{$t('main.bankTransfer')}} {{$t('main.sberbank')}} </span>
          </p>
        </div>
      </div>
    </div>
    <div class="step-2">
      <p><span class="opacity-50">{{$t('sendMoney.step')}} 2: </span> {{$t('sendMoney.approve')}} </p>
      <p v-html="$t('sendMoney.text2')">
      </p>
      <Button
        class="w-100 mt-20"
        green
        @click.native="paid"
        :disabled="invoice.status !== 'waiting_for_payment'"
      >{{$t('sendMoney.payed')}}
      </Button>
    </div>
    <div class="step-3" v-if="invoice.status === 'waiting_for_tokens'">
      <p><span class="opacity-50">{{$t('sendMoney.step')}} 3: </span> {{$t('sendMoney.wait')}} </p>
      <p v-html="$t('sendMoney.text3')">
      </p>
    </div>
  </div>
</template>

<script>
import Button from '~/components/app/Button'
import formatCurrency from '~/mixins/formatCurrency'

export default {
  mixins: [formatCurrency],
  props: {
    invoice: Object
  },
  components: {
    Button
  },
  methods: {
    paid() {
      this.$store.dispatch('invoice/confirmInvoice', this.invoice._id)
    }
  }
}
</script>

<style lang="scss">
.steps {
  max-width: 550px;
  min-height: 300px;
  width: 100%;
  height: 100%;

  & > * {
    margin-bottom: 40px;
  }

  .steps-list {
    margin-top: 20px;
    padding: 40px;
    &__row {

      display: flex;
      justify-content: space-between;
      // flex-direction: column;

      span {
        text-align: left;

      }
    }

    &--left {
    }
  }
}
</style>
