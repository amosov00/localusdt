<template lang="pug">
  section.hero
    h1 {{ $t('main.buyAndSell') }}
      span.green  USDT (Tether)
    p.paragraph-1  {{ $t('main.simpleFastSafe') }}
    nuxt-link(to="/signup")
      Button(orange rounded lg) {{ $t('main.safeReg') }}
</template>

<script>
import Button from '~/components/app/Button'

export default {
  components: { Button }
}
</script>

<style lang="scss" scoped>
.hero {
  text-align: center;
  margin-top: 90px;

  .paragraph-1 {
    margin-top: 10px;
  }

  .button {
    margin-top: 40px;
  }
}
</style>
