<template>
  <section class="ad">
    <header class="ad__header">
      <h1 class="ad__title">Контакт № {{ invoice._id }}</h1>
      <span class="opacity-50 fz-20"
        >Покупка {{ commaSplitting(invoice.amount_usdt) }} USDT на
        {{ commaSplitting(invoice.amount_rub) }} ₽</span
      >
      <p class="ad__payment-method">
        <!-- <span class="opacity-50">Банковский перевод: </span>{{ ad.bank_title }} -->
      </p>
      <div class="ad__subtitle">
        <p>
          <span class="green">Статус сделки: </span>
          {{ invoiceStatus(invoice.status) }}
        </p>
        <p
          class="underline-link red"
          v-if="invoice.status === 'waiting_for_payment'"
          @click="cancel"
        >
          Отменить сделку
        </p>
      </div>
    </header>
    <main class="body">
      <div class="body__info">
        <div class="box">
          <p class="body__field">Цена:</p>
          <p class="body__field">
            {{ commaSplitting(invoice.amount_rub) }} ₽/USDT
          </p>
        </div>
        <div class="box" v-if="invoice.ads_type === 1">
          <p class="body__field">Продавец:</p>
          <p class="body__field">{{ invoice.seller_username }}</p>
        </div>
        <div class="box" v-else-if="invoice.ads_type === 2">
          <p class="body__field">Покупатель:</p>
          <p class="body__field">{{ invoice.buyer_username }}</p>
        </div>
        <hr />
        <div class="box">
          <p class="body__field">Способ оплаты:</p>
          <p class="body__field">Банковский перевод: Сбербанк</p>
        </div>
        <div class="box">
          <p class="body__field">Ограничения по сделке:</p>
        </div>
        <div class="box">
          <p class="body__field">Местоположение:</p>
          <p class="body__field">Российская Федерация</p>
        </div>
        <div class="box">
          <p class="body__field">Окно оплаты:</p>
          <p class="body__field">1 час 30 минут</p>
        </div>
      </div>
      <div class="condition">
        <h2 class="condition__title">Условия сделки</h2>
        <div class="condition__box"></div>
      </div>
    </main>
    <div class="ad__footer">
      <div class="chat"></div>
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
            Токены удерживаются на счете в течение <span class="orange">90 минут</span>, за это время
            необходимо осуществить оплату. После оплаты Вам необходимо <span class="orange"> отметить
            платеж как завершенный</span>, нажав на кнопку “я заплатил”, в противном
            случае сделка будет автоматически отменена.
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
          <p>В течении <span class="orange">30 минут</span> продавец отпрвит токены на ваш адрес.</p>
        </div>
      </div>
    </div>
    <!-- <Modal /> -->
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import formatCurrency from '~/mixins/formatCurrency'
import invoiceStatuses from '~/mixins/invoiceStatuses'
import Button from '~/components/app/Button'
import Modal from '~/components/app/Modal'
export default {
  name: 'invoice_by_id',
  mixins: [formatCurrency, invoiceStatuses],
  components: {
    Button,
    Modal
  },
  data() {
    return {}
  },
  computed: {
    ...mapGetters({
      invoice: 'invoice/invoiceById'
    })
  },
  methods: {
    cancel() {
      this.$store.dispatch('invoice/cancelInvoice', this.invoice._id)
    },
    paid() {
      // const res = this.$store.dispatch(
      //   'invoice/confirmInvoice',
      //   this.invoice._id
      // )
      // console.log(res)
      // if (res) {
      //   this.$store.dispatch('invoice/fetchInvoiceById', this.invoice._id)
      //   this.$toast.showMessage({
      //     content: 'В течении 30 минут продавец отпрвит токены на ваш адрес.',
      //     green: true
      //   })
      // } else {
      //   this.$toast.showMessage({
      //     content: 'Что-то пошло не так...',
      //     red: true
      //   })
      //   console.log(res.error)
      // }
    },
  },
  asyncData({ route, store }) {
    return store.dispatch('invoice/fetchInvoiceById', route.params.id)
  }
}
</script>

<style lang="scss">
.ad {
  margin-top: 50px;

  &__title {
    display: inline-block;
  }

  &__subtitle {
    display: flex;
    justify-content: space-between;
  }

  &__payment-method {
    margin-top: 20px;
  }

  &__footer {
    margin-top: 30px;
    margin-bottom: 30px;
    display: flex;
    justify-content: space-between;

    .chat {
      max-width: 550px;
      min-height: 300px;
      width: 100%;
      height: 100%;
      background-color: $green;
    }

    .steps {
      max-width: 550px;
      min-height: 300px;
      width: 100%;
      height: 100%;

      & > * {
        margin-bottom: 40px;
      }
    }
  }

  .body {
    margin-top: 10px;
    height: 100%;
    // background-color: $orange;
    border-top: 1px solid $grey;
    border-bottom: 1px solid $grey;
    padding: 50px 0 50px 0;

    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;

    &__info {
      // background-color: $red;
      min-width: 200px;
      max-width: 450px;
      width: 100%;
      display: flex;
      flex-direction: column;

      .box {
        display: flex;
        justify-content: space-between;

        & > * {
          font-size: 14px;
          margin-bottom: 15px;
        }
      }
    }

    .condition {
      min-width: 350px;
      max-width: 500px;
      width: 100%;

      &__box {
        margin-top: 30px;
        background: rgba(72, 177, 144, 0.05);
        border-radius: $border-radius;
        padding: 30px 15px;
      }
    }
  }
}
</style>
