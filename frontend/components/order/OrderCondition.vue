<template>
  <div class="order-condition">
    <h2 class="order-condition__title">Условия сделки</h2>
    <div class="order-condition__box">
      <p class="opacity-50">{{ orderCondition }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    orderCondition: String
  }
}
</script>

<style lang="scss">
.order-condition {
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
