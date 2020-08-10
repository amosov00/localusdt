<template>
  <section class="wallet">
    <div class="wallet__header">
      <div class="wallet__info">
        <h1 class="wallet__title">Кошелек</h1>
      </div>
      <div class="wallet__balance">
        <p class="wallet__amount">231,21 USDT</p>
      <div class="wallet__avaible">
        <p><span class="opacity-50">Доступно:</span> 200 USDT</p>
        <p><span class="opacity-50">В сделках:</span> 31,21 USDT</p>
      </div>
      </div>
    </div>
    <WalletInteraction />
    <WalletTransactions />
  </section>
</template>

<script>
import WalletInteraction from '~/components/wallet/WalletInteraction'
import WalletTransactions from '~/components/wallet/WalletTransactions'
export default {
  name: 'wallet',
  middleware: ['authRequired', 'fetchUser'],
  components: {WalletInteraction, WalletTransactions},
  data() {
    return {}
  }
}
</script>

<style lang="scss">
.wallet {
  &__header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-top: 50px;
    height: 80px;
    border-bottom: 1px solid $grey;
  }

  &__title {
    font-weight: 500;
  }

  &__info {
    display: flex;
    align-items: center;
  }

  &__balance {
    display: flex;
    flex-direction: column;
    // margin-right: 120px;
    margin-right: 200px;
  }

  &__amount {
    @include montserrat;
    font-weight: 500;
    font-size: 40px;
    color: $grey-dark;
  }

  &__avaible {
    display: flex;

    p {
      margin-right: 5px;
    }
  }
}
</style>
