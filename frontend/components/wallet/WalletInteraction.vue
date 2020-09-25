<template>
  <div class="interaction">
    <div class="withdraw">
      <div class="withdraw__header">
        <h2 class="withdraw__title">Вывести USDT</h2>
        <p class="withdraw__subtitle">
          Минимальная сумма отправки <span class="orange">1 USDT</span>
        </p>
      </div>

      <form class="withdraw__form">
        <div class="row">
          <Input
            v-model="withdrawForm.amount"
            type="number"
            header="Сумма перевода"
            :width="150"
          />
        </div>
        <div class="row mt-40">
          <Input
            v-model="withdrawForm.address"
            type="text"
            header="Принимающий адрес"
            :width="400"
          />
          <Button class="ml-30" @click.native="withdrawFunds" :disabled="withdrawBtn" green>Вывести</Button>
        </div>
      </form>
    </div>
    <div class="add">
      <h2 class="add__title">Пополнить USDT</h2>
      <Input
        class="mt-50"
        type="text"
        header="Используйте этот адрес чтобы пополнить баланс"
        :value="user.eth_address"
        disabled
        endIcon="copy"
        :width="400"
      />
    </div>
    <WalletTxModal :show="show" @toggleModal="show = $event" />
  </div>
</template>

<script>
import Button from '~/components/app/Button'
import Input from '~/components/app/Input'
import Select from '~/components/app/Select'
import WalletTxModal from '~/components/WalletTxModal'
import { mapGetters } from 'vuex'
export default {
  components: {
    Button,
    Input,
    Select,
    WalletTxModal
  },
  data() {
    return {
      withdrawBtn: false,
      show: false,
      withdrawForm: {
        amount: 0,
        address: ''
      }
    }
  },
  computed: {
    ...mapGetters({
      user: 'user'
    })
  },
  methods: {
    async withdrawFunds() {
      if (this.withdrawForm.amount <= 0) {
        this.$toast.showMessage({ content: 'Введите сумму', red: true })
      } else if (!this.withdrawForm.address) {
        this.$toast.showMessage({ content: 'Введите адрес', red: true })
      } else {
        this.withdrawBtn = true;

        const res = await this.$store.dispatch('wallet/withdraw', {
          amount: this.withdrawForm.amount,
          to: this.withdrawForm.address
        })

        if(res) {
          this.withdrawForm.amount = ''
          this.withdrawForm.address = ''
          this.show = true
          this.$store.dispatch('wallet/fetchTransactions')
        } else {
          this.$toast.showMessage({ content: 'Что-то пошло не так, попробуйте немного позже', red: true })
        }

        this.withdrawBtn = false;
      }
    }
  }
}
</script>

<style lang="scss">
.interaction {
  margin-top: 50px;
  display: flex;
  justify-content: space-between;

  padding-bottom: 45px;
  border-bottom: 1px solid #e7e8e8;

  .withdraw {
    .row {
      display: flex;
      align-items: flex-start;
    }

    &__header {
      display: flex;
      align-items: center;
    }

    &__title {
      font-weight: 500;
    }

    &__subtitle {
      margin-left: 15px;
      color: $grey-dark;
    }

    &__form {
      margin-top: 50px;
    }
  }

  .add {
    margin-right: 130px;
    &__title {
      font-weight: 500;
    }
  }
}
</style>
