<template>
  <div class="ad-condition">
    <h2 class="ad-condition__title">Условия сделки</h2>
    <div class="ad-condition__box">
      <p class="opacity-50">{{ adCondition }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    adCondition: String
  }
}
</script>

<style lang="scss">
.ad-condition {
  min-width: 350px;
  max-width: 500px;
  width: 100%;

  &__title {
    font-weight: 500;
    font-size: 20px;
  }

  &__box {
    margin-top: 30px;
    background: rgba(72, 177, 144, 0.05);
    border-radius: $border-radius;
    padding: 30px 15px;
  }
}
</style>
