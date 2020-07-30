<template>
  <section class="profile">
    <div class="profile__header">
      <div class="profile__user">
        <h1 class="profile__username">{{ user.username }}</h1>
        <span class="profile__activity"></span>
      </div>
      <div class="profile__actions">
        <nuxt-link class="profile__link profile__link--grey" to="/change"
          >Изменить пароль</nuxt-link
        >
        <p class="profile__link red" @click="logout()">Выйти</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  middleware: ['authRequired'],
  data() {
    return {}
  },
  computed: {
    user() {
      return this.$store.getters.user
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logOut')
    }
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

  &__link {
    text-decoration: underline;
    font-weight: 500;
    font-size: 16px;
    cursor: pointer;

    &:last-child {
      margin-top: 10px;
    }

    &--grey {
      color: rgba(17, 23, 29, 0.5) !important;
    }

    .red {
      color: $red;
    }
  }
}
</style>
