<template>
  <section class="order">
    <header class="order__header">
      <h1 class="ad__title">Контакт № {{ invoice._id }}</h1>
      <span class="opacity-50 fz-20" v-if="invoice.ads_type === 1"
        >Продажа {{ commaSplitting(invoice.amount_usdt) }} USDT на
        {{ commaSplitting(invoice.amount_rub) }} ₽</span
      >
      <span class="opacity-50 fz-20" v-else-if="invoice.ads_type === 2"
        >Покупка {{ commaSplitting(invoice.amount_usdt) }} USDT на
        {{ commaSplitting(invoice.amount_rub) }} ₽</span
      >
      <div class="ad__subtitle">
        <p>
          <span class="green">Статус сделки: </span>
          {{ invoiceStatus(invoice.status) }}
        </p>
        <p
          class="underline-link red"
          v-if="
            invoice.status === 'waiting_for_payment' && invoice.ads_type === 1
          "
          @click="cancelModal = true"
        >
          Отменить сделку
        </p>
      </div>
    </header>
    <OrderInfo :order="invoice" />
    <div class="order__footer">
      <Chat :invoice="invoice" />
      <div v-if="invoice.ads_type === 2">
        <SendMoneySteps
          v-if="userRole === 'owner_buy' || userRole === 'customer_sell'"
          :invoice="invoice"
        />
        <SendUSDTSteps
          v-if="userRole === 'owner_sell' || userRole === 'customer_buy'"
          :invoice="invoice"
        />
      </div>
      <div v-else-if="invoice.ads_type === 1">
        <SendMoneySteps
          v-if="userRole === 'owner_sell' || userRole === 'customer_buy'"
          :invoice="invoice"
        />
        <SendUSDTSteps
          v-if="userRole === 'owner_buy' || userRole === 'customer_sell'"
          :invoice="invoice"
        />
      </div>
    </div>
    <InvoiceCancelModal
      :show="cancelModal"
      @toggleModal="cancelModal = $event"
      :invoice="invoice"
    />
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import formatCurrency from '~/mixins/formatCurrency'
import invoiceStatuses from '~/mixins/invoiceStatuses'
import Button from '~/components/app/Button'
import OrderForm from '~/components/order/OrderForm'
import OrderInfo from '~/components/order/OrderInfo'
import Chat from '~/components/app/Chat'
import SendUSDTSteps from '~/components/invoice/SendUSDTSteps'
import SendMoneySteps from '~/components/invoice/SendMoneySteps'
import InvoiceCancelModal from '~/components/InvoiceCancelModal'
export default {
  name: 'invoice_by_id',
  mixins: [formatCurrency, invoiceStatuses],
  components: {
    Button,
    OrderForm,
    OrderInfo,
    Chat,
    SendUSDTSteps,
    SendMoneySteps,
    InvoiceCancelModal
  },
  data() {
    return {
      cancelModal: false,
      invoiceId: this.$route.params.id,
      interval: null
    }
  },
  computed: {
    ...mapGetters({
      invoice: 'invoice/invoiceById',
      user: 'user'
    }),
    userRole() {
      if (
        this.invoice.ads_type === 1 &&
        this.user.username === this.invoice.buyer_username
      ) {
        return 'owner_buy'
      } else if (
        this.invoice.ads_type === 1 &&
        this.user.username === this.invoice.seller_username
      ) {
        return 'customer_buy'
      }

      if (
        this.invoice.ads_type === 2 &&
        this.user.username === this.invoice.buyer_username
      ) {
        return 'owner_sell'
      } else if (
        this.invoice.ads_type === 2 &&
        this.user.username === this.invoice.seller_username
      ) {
        return 'customer_sell'
      }
    }
  },
  created() {
    this.interval = setInterval(async () => {
      await this.$store.dispatch('invoice/fetchInvoiceById', this.invoiceId)
      if (this.invoice === 'waiting_for_tokens') {
        clearInterval(this.interval)
      }
    }, 3000)
  },
  beforeDestroy() {
    clearInterval(this.interval)
  },
  asyncData({ route, store }) {
    return store.dispatch('invoice/fetchInvoiceById', route.params.id)
  }
}
</script>

<style lang="scss">
.order {
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
