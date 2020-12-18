<template>
  <header class="header">
    <div class="header__container">
      <nuxt-link to="/">
        <img class="header__logo" src="~/assets/icons/logo.svg" alt="Logo" />
      </nuxt-link>
      <nav class="header__nav">
        <ul class="nav">
          <nuxt-link
            v-for="link in footerLinks"
            :key="link.title"
            :to="link.url"
            @click.native="forceReload(link.url)"
            class="nav__item"
          >{{ link.title }}
          </nuxt-link
          >
          <nuxt-link class="nav__item" :to="$userIsLoggedIn() ? '/bid' : '/signup'">
            {{ $t('navbar.newOrder')}}
          </nuxt-link>
          <nuxt-link class="nav__item" :to="'/rates'">
            {{ $t('navbar.rates')}}
          </nuxt-link>
        </ul>
      </nav>
      <div class="header__actions">
        <NotificationCenter class="mr-15" v-if="$userIsLoggedIn()"></NotificationCenter>
        <div v-if="!$userIsLoggedIn()">
          <nuxt-link class="header__action disabled" to="/signup"
          >{{$t('navbar.reg')}}
          </nuxt-link
          >
          <nuxt-link class="header__action" to="/login">{{$t('navbar.signIn')}}</nuxt-link>
        </div>
        <div class="header__user" v-else>
          <nuxt-link to="/wallet" class="header__balance"
          >{{ commaSplitting(user.balance_usdt) }} USDT
          </nuxt-link
          >
          <nuxt-link class="header__action" to="/profile">{{
            user.username
            }}
          </nuxt-link>
        </div>
      </div>
      <div class="header__lang">
        <LangSwitcher />
      </div>
    </div>
  </header>
</template>

<script>
import LangSwitcher from '~/components/app/LangSwitcher'
import formatCurrency from '~/mixins/formatCurrency'
import NotificationCenter from '~/components/app/NotificationCenter'

export default {
  mixins: [formatCurrency],
  components: {
    LangSwitcher, NotificationCenter
  },
  data() {
    return {
      interval: null,
      footerLinks: [
        { title: this.$t('navbar.buy'), url: '/buy' },
        { title: this.$t('navbar.sell'), url: '/sell' }
      ]
    }
  },
  computed: {
    user() {
      return this.$store.getters.user
    }
  },
  methods: {
    forceReload(url) {
      if (this.$route.path === url) {
        window.location.reload()
      }
    }
  },
  mounted() {
    this.interval = setInterval(async() => {
      if (this.user) {
        await this.$store.dispatch('fetchBalance')
      }
    }, 10000)
  },
  beforeDestroy() {
    clearInterval(this.interval)
  },
}
</script>

<style lang="scss">
.header {
  height: 70px;
  width: 100%;
  background-color: $white;
  box-shadow: 0px 2px 7px rgba(0, 0, 0, 0.15);

  &__container {
    max-width: 1230px;
    width: 100%;
    margin: auto;
    height: inherit;
    display: flex;
    align-items: center;
    padding-right: 20px;
    padding-left: 20px;
  }

  &__nav {
    .nav {
      display: flex;
      align-items: center;
      height: 100%;
      &__item {
        margin-left: 40px;
        list-style: none;
        text-decoration: none;
      }
    }
  }

  &__actions {
    display: flex;
    align-items: center;
    margin-left: auto;
  }

  &__action {
    @include reset-link;

    font-family: 'Roboto';
    font-style: normal;
    font-weight: normal;
    font-size: 14px;
  }

  &__user {
    height: 70px;
    display: flex;
    align-items: center;
  }

  &__balance {
    margin-right: 60px;
    position: relative;

    span {
      margin-right: 5px;
    }

    &::after {
      content: '';
      position: absolute;
      top: -26px;
      right: -30px;
      display: block;
      height: 70px;
      width: 1px;
      background-color: $black;
      opacity: 0.2;
    }
  }

  &__lang {
    margin-left: 50px;
  }
}
</style>
