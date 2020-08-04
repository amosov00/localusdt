<template>
  <div class="ad-details">
    <div class="ad-details__row fz-20">
      <p class="ad-details__cell opacity-50">Цена</p>
      <p class="ad-details__cell">{{ commaSplitting(adDetails.price || adDetails.amount_rub) }} ₽/USDT</p>
    </div>
    <div class="ad-details__row">
      <p class="ad-details__cell opacity-50" v-if="adDetails.type || adDetails.ads_type === 1">Продавец:</p>
      <p class="ad-details__cell opacity-50" v-else-if="adDetails.type || adDetails.ads_type === 2">Покупатель:</p>
      <p class="ad-details__cell">{{ adDetails.username || adDetails.buyer_username }}</p>
    </div>
    <div class="ad-details__row">
      <p class="ad-details__cell opacity-50">Способ оплаты:</p>
      <p class="ad-details__cell">Банковский перевод: Сбербанк</p>
    </div>
    <hr>
    <div class="ad-details__row mt-10">
      <p class="ad-details__cell opacity-50">Ограничения по сделке:</p>
      <p class="ad-details__cell" v-if="adDetails.bot_limit && adDetails.top_limit"><span>{{spaceSplitting(adDetails.bot_limit)}}</span> — <span>{{spaceSplitting(adDetails.top_limit)}} ₽</span></p>
    </div>
    <div class="ad-details__row mt-10">
      <p class="ad-details__cell opacity-50">Местоположение:</p>
      <p class="ad-details__cell">Российская Федерация</p>
    </div>
    <div class="ad-details__row mt-10">
      <p class="ad-details__cell opacity-50">Окно оплаты:</p>
      <p class="ad-details__cell">1 час 30 минут</p>
    </div>
  </div>
</template>

<script>
import formatCurreny from '~/mixins/formatCurrency'
export default {
  props: {
    adDetails: Object
  },
  mixins: [formatCurreny]
}
</script>

<style lang="scss">
.ad-details {
  width: 450px;
  font-size: 14px;

  &__row {
    display: flex;
    justify-content: space-between;

    & > * {
      margin-bottom: 15px;
    }
  }

  &__cell {
    flex: 1;
  }
}
</style>