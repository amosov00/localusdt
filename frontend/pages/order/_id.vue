<template>
  <section class="order">
    <header class="order__header">
      <h1 v-if="order.type === 1" class="order__title" >{{$t('profile.buyUSDT')}}</h1>
      <h1 v-else class="order__title">{{$t('profile.sellUSDT')}}</h1>
      <!--<div>{{ order }}</div>-->
      <div class="order__header-additional">
        <div class="order__subtitle flex-1"> {{ order.other_payment_method ? order.other_payment_method : paymentMethod(order.payment_method) }}</div>
        <div class="flex-1 order__header-actions" v-if=" user && order.status < 3 && order.username === user.username">
          <n-link class="order__link order__link--edit" :to="`/bid/${isSell ? 'sell' : 'buy' }?edit=${id}`">
            <InlineSvg :src="require('~/assets/icons/pen.svg')"></InlineSvg>
            <span>{{$t('order.edit')}}</span>
          </n-link>
          <div class="order__link order__link--remove" @click="showModal = true">
            <InlineSvg :src="require('~/assets/icons/trash.svg')"></InlineSvg>
            <span>{{$t('order.delete')}}</span>
          </div>
        </div>
        <div v-else-if="order.status === 3" class="order__deleted">
          {{$t('order.deletedByUser')}}
        </div>
      </div>
    </header>
    <div class="mt-30 mb-30">
      <label for="radio-online" class="radio mr-15">
        <input id="radio-online" type="radio" name="status" value="on" v-model="adStatus">
        <span class="radio__check"></span>
        <span class="radio__text">{{$t('order.online')}}</span>
      </label>
      <label for="radio-offline" class="radio">
        <input id="radio-offline" type="radio" name="status" value="off" v-model="adStatus">
        <span class="radio__check"></span>
        <span class="radio__text">{{$t('order.offline')}}</span>
      </label>
    </div>
    <OrderInfo :order="order" />
    <div class="order__footer">
      <OrderForm :order="order" />
    </div>
    <Confirm :title="$t('order.question')" :show="showModal" @toggleModal="showModal = $event">
      <template v-slot:actions>
        <Button red class="mr-15" @click.native="removeOrder(order._id)">{{$t('order.deleteAd')}}</Button>
        <Button white @click.native="showModal = false">{{$t('other.cancel')}}</Button>
      </template>
    </Confirm>
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import OrderForm from '~/components/order/OrderForm'
import OrderInfo from '~/components/order/OrderInfo'
import InlineSvg from 'vue-inline-svg'
import Button from "~/components/app/Button";
import paymentMethod from '~/mixins/paymentMethod'

import Confirm from "~/components/app/Confirm";

export default {
  name: 'order_by_id',
  components: { OrderInfo, OrderForm, InlineSvg, Confirm, Button },
  mixins: [paymentMethod],
  data: () => ({
    showModal: false,
    adStatus: 'on',
    adChangeError: false,
    adWatcherDisabled: false
  }),

  beforeMount() {
    this.setAdStatus()

    if(this.order.status < 3) {
      this.setWatcher()
    }
  },

  methods: {
    setAdStatus() {
      if(this.order.status === 1) {
        this.adStatus = 'on'
      } else {
        this.adStatus = 'off'
      }
    },

    setWatcher() {
      this.$watch('adStatus', async (newVal, oldVal) => {
        if(this.adWatcherDisabled) {
          return
        }

        if(this.adChangeError) {
          this.adChangeError = false
          return;
        }

        let res = await this.$store.dispatch('order/setOrderStatus', { id: this.order._id, endpoint: this.adStatus })

        if(res) {
          await this.refreshData()
        } else {
          this.adChangeError = true
          this.adStatus = oldVal
        }
      });
    },

    async removeOrder(orderId) {
      if(orderId) {
        await this.$store.dispatch('order/removeOrder', orderId)
        this.showModal = false
        this.adWatcherDisabled = true
        await this.$store.dispatch('order/fetchOrderById', orderId)
      }
    },

    async refreshData() {
      this.$store.dispatch('order/fetchOrderById', this.order._id)
        .then(() => {
          this.setAdStatus()
        })
    }

  },

  computed: {
    ...mapGetters({
      order: 'order/orderById',
      user: 'user'
    }),

    isSell() {
      return this.order.type === 1
    }
  },
  async asyncData({ store, params }) {
    await store.dispatch('order/fetchOrderById', params.id)
    return {
      id: params.id
    }
  }
}
</script>

<style lang="scss" scoped>
.order {
  margin-top: 50px;

  &__title {
    display: block;
    margin-bottom: 17px;
  }

  &__deleted {
    color: #a5a5a5;
    font-size: 14px;
  }

  &__subtitle {
    font-size: 14px;
    line-height: 16px;
    color: #11171D;
    opacity: 0.5;
  }

  &__header-additional {
    display: flex;
    align-items: center;
  }

  &__header-actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }

  &__link {
    font-family: "Roboto", "Montserrat", "Arial", "Tahoma", sans-serif;
    font-style: normal;
    font-weight: 500;
    font-size: 16px;
    line-height: 19px;
    text-align: right;
    text-decoration: underline;
    display: flex;
    align-items: center;
    margin-right: 50px;
    transition: 200ms transform;
    cursor: pointer;

    &:last-child {
      margin-right: 0;
    }

    &:hover {
      text-decoration: none;
    }

    &:active {
      transform: scale(0.96);
    }

    > svg {
      transition: 200ms transform;
    }

    > span {
      margin-left: 10px;
    }

    &--edit {
      color: #ED9F43;
    }

    &--remove {
      color: #B21B11;
    }
  }

  &__payment-method {
    margin-top: 20px;
  }

  &__footer {
    margin-top: 30px;
    margin-bottom: 30px;
  }
}
</style>
