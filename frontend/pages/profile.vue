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
      <invoicesTable :tableData="invoices" />
    </div>
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import invoicesTable from '~/components/app/invoicesTable'
export default {
  middleware: ['authRequired', 'fetchUser'],
  components: {
    invoicesTable
  },
  data() {
    return {}
  },
  computed: {
    // ...mapGetters({
    //   invoices: 'invoice/invoices'
    // }),
    user() {
      return this.$store.getters.user
    },
    invoices() {
      return this.$store.getters['invoice/invoices']
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logOut')
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
}
</style>
