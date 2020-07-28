<template lang="pug">
  section.hero
    h1 Покупка и продажа 
      span.green USDT (Tether)
    p.paragraph-1 Просто, быстро и безопасно
    nuxt-link(to="/signup")
      Button(orange rounded lg) Зарегистрируйтесь бесплатно
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
