<template>
  <section class="ad">
    <header class="ad__header">
      <h1 class="ad__title" v-if="ad.type === 1">Покупка USDT</h1>
      <h1 class="ad__title" v-else>Продажа USDT</h1>
      <p class="ad__payment-method">
        <span class="opacity-50">Банковский перевод: </span>{{ ad.bank_title }}
      </p>
    </header>
    <AdInfo :ad="ad" />
    <div class="ad__footer">
      <AdForm :ad="ad" />
    </div>
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import AdForm from '~/components/AdForm'
import AdInfo from '~/components/AdInfo'
export default {
  name: 'ad_by_id',
  components: {
    AdInfo,
    AdForm
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

  &__payment-method {
    margin-top: 20px;
  }

  &__footer {
    margin-top: 30px;
    margin-bottom: 30px;
  }
}
</style>
