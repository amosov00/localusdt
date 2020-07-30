<template>
  <section class="ad">
    <header class="ad__header">
      <h1 class="ad__title">Покупка USDT</h1>
      <p class="ad__payment-method">
        <span class="opacity-50">Банковский перевод: </span>{{ ad.bank_title }}
      </p>
    </header>
    <main class="body">
      <div class="body__info">
        <div class="box">
          <p class="body__field">Цена:</p>
          <p class="body__field">{{ commaSplitting(ad.price) }} ₽/USDT</p>
        </div>
        <div class="box">
          <p class="body__field">Продавец:</p>
          <p class="body__field">{{ ad.username }}</p>
        </div>
        <hr />
        <div class="box">
          <p class="body__field">Способ оплаты:</p>
          <p class="body__field">Банковский перевод: Сбербанк</p>
        </div>
        <div class="box">
          <p class="body__field">Ограничения по сделке:</p>
          <p class="body__field">{{ad.bot_limit}} - {{spaceSplitting(ad.top_limit)}} ₽</p>
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
        <div class="condition__box">
          <p class="opacity-50">{{ ad.condition }}</p>
        </div>
      </div>
    </main>
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import formatCurreny from '~/mixins/formatCurrency'
export default {
  name: 'ad_by_id',
  mixins: [formatCurreny],
  data() {
    return {}
  },
  computed: {
    ...mapGetters({
      ad: 'ads/adById'
    })
  },
  asyncData({ store, params }) {
    return store.dispatch('ads/fetchAdById', params.id)
  }
}
</script>

<style lang="scss">
.ad {
  margin-top: 50px;

  &__header {
  }

  &__title {
  }

  &__payment-method {
    margin-top: 20px;
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
