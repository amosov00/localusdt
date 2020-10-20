<template>
  <div class="ad-details">
    <div class="order-details__row fz-20">
      <p class="order-details__cell grey-dark">Цена</p>
      <p class="order-details__cell">
        {{ commaSplitting(orderDetails.price || orderDetails.amount) }}
        ₽/USDT
      </p>
    </div>
    <div class="order-details__row" v-if="role && roleUser">
      <p class="order-details__cell grey-dark">
        {{ role }}:
      </p>
      <p class="order-details__cell">
        {{ roleUser }}
      </p>
    </div>
    <div class="order-details__row">
      <p class="order-details__cell grey-dark">Способ оплаты:</p>
      <p class="order-details__cell">Банковский перевод: Сбербанк</p>
    </div>
    <hr />
    <div class="order-details__row mt-10">
      <p class="order-details__cell grey-dark">Ограничения по сделке:</p>
      <p class="order-details__cell">
        <span>{{ spaceSplitting(orderDetails.bot_limit) }}</span> —
        <span>{{ spaceSplitting(orderDetails.top_limit) }} ₽</span>
      </p>
    </div>
    <div class="order-details__row mt-10">
      <p class="order-details__cell grey-dark">Количество:</p>
      <p class="order-details__cell">
        <span>{{ spaceSplitting(orderDetails.amount_usdt) }} USDT</span>
      </p>
    </div>
    <div class="order-details__row mt-10">
      <p class="order-details__cell grey-dark">Местоположение:</p>
      <p class="order-details__cell">Российская Федерация</p>
    </div>
    <div class="order-details__row mt-10">
      <p class="order-details__cell grey-dark">Окно оплаты:</p>
      <p class="order-details__cell">1 час 30 минут</p>
    </div>
  </div>
</template>

<script>
import formatCurreny from '~/mixins/formatCurrency'
import { mapGetters } from 'vuex'
export default {
  props: {
    orderDetails: Object,
  },
  computed: {
    ...mapGetters({
      user: 'user',
    }),
    role() {
      if (
        (this.orderDetails.ads_type || this.orderDetails.type === 1) &&
        this.orderDetails.seller_username === this.user.username
      ) {
        return 'Покупатель'
      } else if (
        (this.orderDetails.ads_type || this.orderDetails.type === 2) &&
        this.orderDetails.buyer_username === this.user.username
      ) {
        return 'Продавец'
      }
    },
    roleUser() {
      switch (this.role) {
        case 'Покупатель':
          return this.orderDetails.buyer_username
          break;
        case 'Продавец':
          return this.orderDetails.username || this.orderDetails.seller_username
          break;
        default:
          break;
      }
    }
  },
  mixins: [formatCurreny],
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
