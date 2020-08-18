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
    <invoicesTable :tableData="invoices" />
  </section>
</template>

<script>
import { mapGetters } from 'vuex'
import invoicesTable from '~/components/app/invoicesTable'
import ProfileReferral from '~/components/ProfileReferral'
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
export default {
  middleware: ['authRequired', 'fetchUser'],
  components: {
    invoicesTable,
    ProfileReferral,
    Textarea,
    Button
  },
  data() {
    return {}
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
