<template>
  <main class="order-info">
    <OrderDetails :orderDetails="order" />
    <OrderCondition :orderCondition="order.condition" />
  </main>
</template>

<script>
import OrderDetails from '~/components/order/OrderDetails'
import OrderCondition from '~/components/order/OrderCondition'
export default {
  props: {
    order: Object
  },
  components: {
    OrderDetails,
    OrderCondition
  }
}
</script>

<style lang="scss">
.order-info {
  margin-top: 10px;
  height: 100%;
  border-top: 1px solid $grey;
  border-bottom: 1px solid $grey;
  padding: 50px 0 50px 0;

  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
</style>
