<template>
  <transition name="fade">
    <div class="modal-wrapper" v-show="show">
      <span @click="hideModal" class="modal-wrapper__cross">
        <img src="~/assets/icons/cross.svg" alt="cross">
      </span>
      <div class="referral">
        <h1 class="referral__title">{{$t('other.sendUSDT')}}</h1>
        <p class="mt-20 fz-20">
          {{ commaSplitting(invoice.amount_usdt) }} USDT {{ $t('other.for') }}
          <span class="opacity-50">
            {{ commaSplitting(invoice.amount) }} ₽
          </span>
        </p>
        <p class="fz-14 mt-20">{{ userName }} <span class="status-circle"></span></p>
        <div>
          <Button @click.native="confirm" class="referral__button mr-15" green lg>
            {{$t('other.send')}}
          </Button>
          <Button @click.native="hideModal" class="referral__button" white lg>
            {{$t('other.cancel')}}
          </Button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import Button from '~/components/app/Button'
import formatCurrency from '~/mixins/formatCurrency'

export default {
  props: {
    show: Boolean,
    invoice: Object
  },
  mixins: [formatCurrency],
  components: {
    Button
  },
  computed: {
    userName() {
      return this.invoice.ads_type === 2
        ? this.invoice.seller_username
        : this.invoice.seller_username
    }
  },
  methods: {
    hideModal() {
      this.$emit('toggleModal', !this.show)
    },
    confirm() {
      this.$store.dispatch('invoice/transferInvoice', this.invoice._id)
      this.hideModal()
    }
  }
}
</script>

<style lang="scss" scoped>
.status-circle {
  display: inline-block;
  width: 10px;
  height: 10px;
  background-color: $green;
  border-radius: 50%;
}
.modal-wrapper {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  -webkit-backdrop-filter: blur(40px);
  backdrop-filter: blur(40px);
  z-index: 100000000000000;

  &__cross {
    position: absolute;
    top: 60px;
    right: 60px;
    cursor: pointer;
  }

  .invoice-confirm {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    &__title {
      font-weight: 500;
    }

    &__condition {
      text-align: center;
      @include montserrat;
      overflow: scroll;
      font-size: 12px;
    }

    &__button {
      margin-top: 80px;
    }

    &__actions {
      margin-top: 90px;
      display: flex;
    }
  }
}
</style>
