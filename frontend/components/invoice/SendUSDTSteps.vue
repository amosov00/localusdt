<template>
  <div class="steps">
    <p class="fz-20">{{ $t('sendSteps.sendTokens') }}</p>
    <p v-html="$t('sendSteps.text1')">
    </p>
    <div class="ma-0 pa-20">
      <p>
        <span class="opacity-50">
          {{$t('sendSteps.text2')}}
        </span>
      </p>
    </div>
    <Button class="w-100 mt-20" green
            :disabled="sendTokenBtn"
            @click.native="confirmationModal = true">
      {{sendTokenBtnText}}
    </Button>
    <InvoiceConfirmationModal
      @toggleModal="confirmationModal = $event"
      :invoice="invoice"
      :show="confirmationModal"
    />
  </div>
</template>

<script>
import Button from '~/components/app/Button'
import InvoiceConfirmationModal from '~/components/InvoiceConfirmationModal'

export default {
  props: {
    invoice: Object
  },
  components: {
    Button,
    InvoiceConfirmationModal
  },
  data() {
    return {
      confirmationModal: false
    }
  },
  computed: {
    sendTokenBtn() {
      const { status } = this.invoice
      return status === 'completed' || status === 'waiting_for_payment' || status === 'cancelled'
    },
    sendTokenBtnText() {
      const { status } = this.invoice
      if (status === 'cancelled') {
        return this.$t('sendSteps.orderCancelled')
      }
      return this.$t('sendSteps.sendTokens')
    }
  },
  methods: {
    paid() {
      this.$emit('showConfirmationModal', true)
    },
    showModal(state) {
      this.confirmationModal = state
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
}
</style>
