<template>
  <transition name="fade">
  <div class="modal-wrapper" v-show="show">
    <div class="referral">
      <h1 class="referral__title">Вы хотите отменить сделку?</h1>
      <p class="fz-20"> Подтвердите отмену сделки с <span class="orange">{{userName}}</span></p>
      <div class="invoice-confirm__actions"></div>
      <Button @click.native="cancel" class="referral__button" red lg>отменить сделку</Button>
      <Button @click.native="hideModal" class="referral__button" white lg>отмена</Button>
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
      return this.invoice.ads_type === 2 ? this.invoice.seller_username : this.invoice.seller_username
    }
  },
  methods: {
    hideModal() {
      this.$emit('toggleModal', !this.show)
    },
    cancel() {
      this.$store.dispatch('invoice/cancelInvoice', this.invoice._id)
      this.hideModal()
    }
  }
}
</script>

<style lang="scss">
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

  .referral {
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

  }
}
</style>