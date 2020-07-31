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
          <span class="green">Статус сделки: </span> Ожидание подтверждения
          платежа покупателем
        </p>
        <p class="underline-link red" v-if="!isPaid" @click="cancel">Отменить сделку</p>
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
        <div class="box">
          <p class="body__field">Продавец:</p>
          <p class="body__field">{{ invoice.seller_username }}</p>
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
      <Button green @click.native="paid" :disabled="isPaid">Я заплатил</Button>
    </div>
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import formatCurrency from '~/mixins/formatCurrency'
import Button from '~/components/app/Button'
export default {
  name: 'invoice_by_id',
  mixins: [formatCurrency],
  components: {
    Button
  },
  data() {
    return {
      isPaid: false
    }
  },
  computed: {
    ...mapGetters({
      invoice: 'invoice/invoiceById'
    })
  },
  methods: {
    cancel() {
      this.$store.dispatch('invoice/cancelInvoice', this.$route.params.id)
    },
    paid() {
      const res = this.$store.dispatch('invoice/confirmInvoice', this.$route.params.id)
      console.log(res)
      if(res) {
        this.isPaid = true
        this.$toast.showMessage({
          content: 'В течении 30 минут продавец отпрвит токены на ваш адрес.',
          green: true
        })
      }
    }
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
