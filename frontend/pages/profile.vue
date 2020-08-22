<template>
  <section class="profile">
    <div class="profile__header">
      <div class="profile__user">
        <h1 class="profile__username">{{ user.username }}</h1>
        <span class="profile__activity"></span>
      </div>
      <div class="profile__actions">
        <nuxt-link class="underline-link underline-link--grey" to="/change"
          >Изменить пароль</nuxt-link
        >
        <p class="underline-link red" @click="logout()">Выйти</p>
      </div>
    </div>
    <div class="bio">
      <div class="bio__container">
        <h2 class="bio__title">О себе</h2>
        <Textarea v-model="condition" />
        <Button @click.native="setCondition" class="mt-20" green
          >Сохранить</Button
        >
      </div>
      <ProfileReferral />
    </div>
    <AppTable :data="invoices" :headers="headers" pagination>
      <template slot-scope="header"></template>
      <template slot-scope="{ row }">
        <td class="table__data">{{timestampToUtc(row.created_at)}}</td>
        <td class="table__data" v-if="row.ads_type === 1">Продажа USDT</td>
        <td class="table__data" v-else-if="row.ads_type === 2"> Покупка USDT</td>
        <td class="table__data">
          {{row.seller_username}}
          <span class="status green--bg" />
          <span class="orders-count">(10+)</span>
        </td>
        <td class="table__data">{{commaSplitting(row.amount_usdt)}} <span class="grey-dark fw-400">за {{commaSplitting(row.amount_rub)}} ₽</span> </td>
        <td class="table__data" :style="{ color: statusColor(row.status) }">
          <nuxt-link :to="`/invoice/${row._id}`">{{invoiceStatusShort(row.status)}}</nuxt-link>
        </td>
      </template>
    </AppTable>
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import invoicesTable from '~/components/app/invoicesTable'
import ProfileReferral from '~/components/ProfileReferral'
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
import AppTable from '~/components/app/AppTable'
import formatCurreny from '~/mixins/formatCurrency'
import formatDate from '~/mixins/formatDate'
import invoiceStatuses from '~/mixins/invoiceStatuses'
export default {
  name: 'profile',
  middleware: ['authRequired', 'fetchUser'],
  mixins: [formatCurreny, formatDate, invoiceStatuses],
  components: {
    invoicesTable,
    ProfileReferral,
    Textarea,
    Button,
    AppTable
  },
  data() {
    return {
      headers: ['Дата, время', 'Вид сделки', 'Покупатель/продавец', 'Сумма', 'Статус']
    }
  },
  computed: {
    user() {
      return { ...this.$store.getters.user }
    },
    invoices() {
      return this.$store.getters['invoice/invoices']
    },
    condition: {
      get: function() {
        return this.user.about_me
      },
      set: function(value) {
        this.user.about_me = value
      }
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logOut')
    },
    setCondition() {
      this.$store.dispatch('changeCondition', this.user.about_me)
    }
  },
  asyncData({ store }) {
    return store.dispatch('invoice/fetchInvoices')
  }
}
</script>

<style lang="scss">
.profile {
  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 50px;
    padding-bottom: 40px;
    border-bottom: 1px solid $grey;
  }

  &__user {
    display: flex;
    align-items: center;
  }

  &__activity {
    display: block;
    margin-left: 20px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background-color: $green;
  }

  &__actions {
    display: flex;
    flex-direction: column;
    text-align: right;
  }

  .bio {
    margin-top: 50px;
    display: flex;
    justify-content: space-between;

    &__title {
      margin-bottom: 35px;
      font-weight: 500;
    }
  }
}
</style>
