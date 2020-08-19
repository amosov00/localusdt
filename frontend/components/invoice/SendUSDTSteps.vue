<template>
  <div class="steps">
    <p class="fz-20">Отправить токены</p>
    <p>
      Покупатель еще не отметил платеж как завершенный, и остается
      <span class="green">89 минут</span> для проведения оплаты. Если оплата не
      будет осуществлена, сделка автоматически отменится. Когда Вы получите
      платеж, <span class="orange">отправьте токены</span> из депонирования.
    </p>
    <div class="ma-0 pa-20">
      <p>
        <span class="opacity-50"
          >Не забудьте дать покупателю указания об оплате</span
        >
      </p>
    </div>
    <Button class="w-100 mt-20" green :disabled="invoice.status === 'completed' || invoice.status === 'waiting_for_payment'" @click.native="confirmationModal = true"
      >отправить токены</Button
    >
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
