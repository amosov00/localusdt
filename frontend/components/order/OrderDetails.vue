<template>
  <div class="ad-details">
    <div class="order-details__row fz-20">
      <p class="order-details__cell opacity-50">Цена</p>
      <p class="order-details__cell">
        {{ commaSplitting(orderDetails.price || orderDetails.amount_rub) }}
        ₽/USDT
      </p>
    </div>
    <div class="order-details__row">
      <p class="order-details__cell opacity-50">
        {{ owner.role }}
      </p>
      <p class="order-details__cell">
        {{ owner.name }}
      </p>
    </div>
    <div class="order-details__row">
      <p class="order-details__cell opacity-50">Способ оплаты:</p>
      <p class="order-details__cell">Банковский перевод: Сбербанк</p>
    </div>
    <hr />
    <!-- temp fix -->
    <div class="order-details__row mt-10" v-if="orderDetails.bot_limit || orderDetails.top_limit">
      <p class="order-details__cell opacity-50">Ограничения по сделке:</p>
      <p
        class="order-details__cell">
        <span>{{ spaceSplitting(orderDetails.bot_limit) }}</span> —
        <span>{{ spaceSplitting(orderDetails.top_limit) }} ₽</span>
      </p>
    </div>
    <div class="order-details__row mt-10">
      <p class="order-details__cell opacity-50">Местоположение:</p>
      <p class="order-details__cell">Российская Федерация</p>
    </div>
    <div class="order-details__row mt-10">
      <p class="order-details__cell opacity-50">Окно оплаты:</p>
      <p class="order-details__cell">1 час 30 минут</p>
    </div>
  </div>
</template>

<script>
import formatCurreny from '~/mixins/formatCurrency'
export default {
  props: {
    orderDetails: Object
  },
  computed: {
    owner() {
      switch (this.orderDetails.type || this.orderDetails.ads_type) {
        case 1:
          return { name: this.orderDetails.username || this.orderDetails.buyer_username, role: 'Продавец:' }
          break
        case 2:
          return { name: this.orderDetails.username || this.orderDetails.seller_username, role: 'Покупатель:' }
          break
      }
    }
  },
  mixins: [formatCurreny]
}
</script>

<style lang="scss">
.order-details {
  width: 450px;
  font-size: 14px;

  &__row {
    display: flex;
    justify-content: space-between;

    &:first-child {
      margin-bottom: 50px;
    }

    & > * {
      margin-bottom: 15px;
    }
  }

  &__cell {
    flex: 1;
  }
}
</style>
