<template>
  <div class="interaction">
    <div class="withdraw">
      <div class="withdraw__header">
        <h2 class="withdraw__title">{{$t('wallet.withdrawUSDT')}}</h2>
        <p class="withdraw__subtitle">
          {{$t('wallet.minSend')}} <span class="orange">1 USDT</span>
        </p>

      </div>
      <p style="margin-left:0;margin-top:10px;" class="withdraw__subtitle">
        {{$t('wallet.description')}}
      </p>
      <form class="withdraw__form">
        <div class="row">
          <Input
            v-model="withdrawForm.amount"
            type="number"
            :header="$t('wallet.transferAmount')"
            :width="150"
          />
        </div>
        <div class="row mt-40">
          <Input
            v-model="withdrawForm.address"
            type="text"
            :header="$t('wallet.receivingAddress')"
            :width="400"
          />
          <Button
            class="ml-30"
            @click.native="withdrawFunds"
            :disabled="withdrawBtn"
            green>
            {{$t('wallet.withdraw')}}
          </Button>
        </div>
      </form>
    </div>
    <div class="add">
      <h2 class="add__title">{{$t('wallet.topUp')}}</h2>
       <p style="margin-left:0; margin-top:10px;" class="withdraw__subtitle">
          {{$t('wallet.descriptionReceive')}}
        </p>
      <Input
        class="mt-50 input-width"
        type="text"
        :header="$t('wallet.balanceAddress')"
        :value="user.eth_address"
        disabled
        endIcon="copy"
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
        this.$toast.showMessage({ content: this.$t('wallet.editSum'), red: true })
      } else if (!this.withdrawForm.address) {
        this.$toast.showMessage({ content: this.$t('wallet.editAddress'), red: true })
      } else {
        this.withdrawBtn = true

        const res = await this.$store.dispatch('wallet/withdraw', {
          amount: this.withdrawForm.amount,
          to: this.withdrawForm.address
        })

        if (res) {
          this.withdrawForm.amount = ''
          this.withdrawForm.address = ''
          this.show = true
          this.$store.dispatch('wallet/fetchTransactions')
        } else {
          this.$toast.showMessage({ content: this.$t('wallet.error'), red: true })
        }

        this.withdrawBtn = false
      }
    }
  }
}
</script>

<style lang="scss">
.input-width {
  //max-width: 400px;
  //width: 100%;
  //display: block;
  @media (max-width: 606px) {
    margin-right: 0;
  }
}
.interaction {
  margin-top: 50px;
  @media (max-width: 966px) {
    display: block;
  }
  display: flex;
  justify-content: space-between;

  padding-bottom: 45px;
  border-bottom: 1px solid #e7e8e8;

  .withdraw {
    @media (max-width: 966px) {
      margin-bottom: 40px;
    }
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
    @media (max-width: 650px) {
      margin-right: 0;
    }
    &__title {
      font-weight: 500;
    }
  }
}
</style>
