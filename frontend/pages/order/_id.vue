<template>
  <section class="order">
    <header class="order__header">
      <div v-if="order.type === 1">
        <h1 class="order__title" >Продажа USDT</h1>
        <n-link :to="`/bid/sell?edit=${id}`">Редактировать</n-link>
      </div>
      <div v-else>
        <h1 class="order__title">Покупка USDT</h1>
        <n-link :to="`/bid/sell?edit=${id}`">Редактировать</n-link>
      </div>
    </header>
    <OrderInfo :order="order" />
    <div class="order__footer" v-if="user.username !== order.username">
      <OrderForm :order="order" />
    </div>
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import OrderForm from '~/components/order/OrderForm'
import OrderInfo from '~/components/order/OrderInfo'
export default {
  name: 'order_by_id',
  components: {
    OrderInfo,
    OrderForm
  },
  computed: {
    ...mapGetters({
      order: 'order/orderById',
      user: 'user'
    })
  },
  asyncData({ store, params }) {
    store.dispatch('order/fetchOrderById', params.id)
    return {
      id: params.id
    }
  }
}
</script>

<style lang="scss">
.order {
  margin-top: 50px;

  &__payment-method {
    margin-top: 20px;
  }

  &__footer {
    margin-top: 30px;
    margin-bottom: 30px;
  }
}
</style>
