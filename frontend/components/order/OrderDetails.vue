<template>
  <div class="ad-details">
    <div class="order-details__row fz-20">
      <p class="order-details__cell grey-dark">{{ $t('orderDetails.price') }}</p>
      <p class="order-details__cell">
        {{ commaSplitting(orderDetails.price || orderDetails.amount) }}
        ₽/USDT
      </p>
    </div>
    <div class="order-details__row" v-if="role && roleUser">
      <p class="order-details__cell grey-dark">
        {{ roleHumanize }}:
      </p>
      <p class="order-details__cell">
        {{ roleUser }}
      </p>
    </div>
    <div class="order-details__row">
      <p class="order-details__cell grey-dark">{{ $t('orderDetails.payType') }}</p>
      <p class="order-details__cell">{{ $t('main.bankTransfer') }} {{ $t('main.sberbank') }}</p>
    </div>
    <hr />
    <div class="order-details__row mt-10">
      <p class="order-details__cell grey-dark">{{ $t('orderDetails.limits') }}</p>
      <p class="order-details__cell">
        <span>{{ spaceSplitting(orderDetails.bot_limit) }}</span> —
        <span>{{ spaceSplitting(orderDetails.top_limit) }} USDT</span>
      </p>
    </div>
    <div class="order-details__row mt-10">
      <p class="order-details__cell grey-dark">{{ $t('orderDetails.quantity') }}</p>
      <p class="order-details__cell">
        <span>{{ spaceSplitting(orderDetails.amount_usdt) }} USDT</span>
      </p>
    </div>
    <div class="order-details__row mt-10">
      <p class="order-details__cell grey-dark">{{ $t('orderDetails.place') }}</p>
      <p class="order-details__cell">{{ $t('orderDetails.rf') }}</p>
    </div>
    <div class="order-details__row mt-10">
      <p class="order-details__cell grey-dark">{{ $t('orderDetails.timeLimit') }}</p>
      <p class="order-details__cell">
        1 {{ $t('orderDetails.hour') }} 30 {{ $t('orderDetails.min') }}
      </p>
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
        return 'bayer'
      } else if (
        (this.orderDetails.ads_type || this.orderDetails.type === 2) &&
        this.orderDetails.buyer_username === this.user.username
      ) {
        return 'seller'
      }
    },
    roleHumanize() {
      switch (this.role) {
        case 'bayer':
          return this.$t('orderDetails.bayer')
          break
        case 'seller':
          return this.$t('orderDetails.seller')
          break
        default:
          return ''
          break
      }
    },
    roleUser() {
      switch (this.role) {
        case 'bayer':
          return this.orderDetails.buyer_username
          break
        case 'seller':
          return this.orderDetails.username || this.orderDetails.seller_username
          break
        default:
          break
      }
    },
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
