<template>
  <main class="ad-info">
    <AdDetails :adDetails="ad" />
      <AdCondition :adCondition="ad.condition" />
  </main>
</template>

<script>
import AdDetails from '~/components/AdDetails'
import AdCondition from '~/components/AdCondition'
export default {
  props: {
    ad: Object
  },
  components: {
    AdDetails,
    AdCondition
  }
}
</script>

<style lang="scss">
  .ad-info {
    margin-top: 10px;
    height: 100%;
    border-top: 1px solid $grey;
    border-bottom: 1px solid $grey;
    padding: 50px 0 50px 0;

    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
  }
</style>