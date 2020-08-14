<template>
  <div class="steps">
    <div class="step-1">
      <p><span class="opacity-50">Шаг 1: </span> Заплатите продавцу</p>
      <p>
        Отправьте сообщение (имя продавца), чтобы обратиться за помощью в
        совершении платежа.
      </p>
      <div class="mt-20 pa-20">
        <p><span class="opacity-50">Сумма: </span><span>7044,00 ₽</span></p>
        <p>
          <span class="opacity-50">Способ оплаты: </span>
          <span>Банковский перевод: Сбербанк</span>
        </p>
      </div>
    </div>
    <div class="step-2">
      <p><span class="opacity-50">Шаг 2: </span> Подтвердите платеж</p>
      <p>
        Токены удерживаются на счете в течение
        <span class="orange">90 минут</span>, за это время необходимо
        осуществить оплату. После оплаты Вам необходимо
        <span class="orange"> отметить платеж как завершенный</span>, нажав на
        кнопку “я заплатил”, в противном случае сделка будет автоматически
        отменена.
      </p>
      <Button
        class="w-100 mt-20"
        green
        @click.native="paid"
        :disabled="invoice.status !== 'waiting_for_payment'"
        >Я заплатил</Button
      >
    </div>
    <div class="step-3" v-if="invoice.status === 'waiting_for_tokens'">
      <p><span class="opacity-50">Шаг 3: </span> Ожидайте токены</p>
      <p>
        В течении <span class="orange">30 минут</span> продавец отпрвит токены
        на ваш адрес.
      </p>
    </div>
  </div>
</template>

<script>
import Button from '~/components/app/Button'
export default {
  props: {
    invoice: Object
  },
  components: {
    Button
  },
  methods: {
    paid() {
      console.log('paid')
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
}
</style>
