<template lang="pug">
div.bid-type
  header.bid-type__header
    h1.bid-type__title {{ $t('bid.title') }}
    p.paragraph-1.bid-type__subtitle {{ $t('bid.subtitle') }}
  div.bid-type__body
    nuxt-link.bid-type__link(to="/bid/sell/")
      InlineSvg(:src="require('~/assets/icons/sell-bid.svg')")
      span.bid-type__text {{ $t('bid.sellUSDT') }}
    nuxt-link.bid-type__link(to="/bid/buy/")
      InlineSvg(:src="require('~/assets/icons/buy-bid.svg')")
      span.bid-type__text {{ $t('bid.buyUSDT') }}
</template>

<script>
import InlineSvg from 'vue-inline-svg'

export default {
  middleware: ['authRequired'],
  components: { InlineSvg }
}
</script>

<style lang="scss">
.bid-type {
  margin: 0 auto;
  max-width: 500px;
  width: 100%;
  text-align: center;
  padding-top: 130px;

  &__text {
    opacity: 0.5;
    line-height: 24px;
    font-size: 20px;
    font-weight: 500;
  }

  &__header {
    margin-bottom: 90px;
  }

  &__link {
    @include reset-link;
    height: 180px;
    width: 160px;
  }

  &__body {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
}
</style>
