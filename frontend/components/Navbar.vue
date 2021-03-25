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
          <nuxt-link class="header__action disabled" to="/login">{{$t('navbar.signIn')}}</nuxt-link>
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
      <NotificationCenter class="mr-15" style="margin-left: auto;" v-if="$userIsLoggedIn() && windowWidth < 916"></NotificationCenter>
      <button
        class="navbar-toggle"
        @click="dialog = !dialog"
        :class="[
        {
          'navbar-toggle-active': dialog
        },
        {
          'navbar-margin': !$userIsLoggedIn()
        }
        ]"

      >
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
    </div>
    <transition name="dialog">
      <div class="header__dialog" v-if="dialog">
      <nav class="nav">
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
          <nuxt-link
            class="nav__item"
            :to="$userIsLoggedIn() ? '/bid' : '/signup'"
            @click.native="dialog = false"
          >
            {{ $t('navbar.newOrder')}}
          </nuxt-link>
          <nuxt-link
            class="nav__item"
            :to="'/rates'"
            @click.native="dialog = false"
          >
            {{ $t('navbar.rates')}}
          </nuxt-link>
        </ul>
      </nav>
      <div class="actions">
        <div v-if="!$userIsLoggedIn()">
          <span></span>
          <nuxt-link class="header__action disabled" to="/signup" @click.native="dialog = false"
          >{{$t('navbar.reg')}}
          </nuxt-link
          >
          <nuxt-link class="header__action disabled" to="/login" @click.native="dialog = false">{{$t('navbar.signIn')}}</nuxt-link>
        </div>
        <div class="header__user block" v-else>
          <nuxt-link
            class="align-flex"
            to="/wallet"
            @click.native="dialog = false"
          >
            <div>
              <img src="~assets/icons/cash-multiple.svg" alt="cash" class="mr-5">
            </div>
            <div>
              <span class="mr-15">{{$t('wallet.wallet')}}: </span>
              <span
                class="header__balance"
              >
                {{ commaSplitting(user.balance_usdt) }} USDT
              </span>
            </div>
          </nuxt-link>
          <nuxt-link
            class="align-flex"
            @click.native="dialog = false"
            to="/profile"
            tag="div"
          >
            <div>
              <img src="~assets/icons/account-box.svg" alt="account" class="mr-5">
            </div>
            <div>
              <span class="mr-15">{{$t('wallet.profile')}}: </span>
              <span
                class="header__action"
              >
                {{user.username}}
              </span>
            </div>
          </nuxt-link>
        </div>
      </div>
      <div class="align-flex">
        <img src="~assets/icons/earth.svg" alt="earth" class="mr-5">
        <LangSwitcher />
      </div>
        <div
          @click="logout"
          class="margin-zero align-flex"
          v-if="$userIsLoggedIn()"
        >
          <img src="~assets/icons/exit-to-app.svg" alt="exit" class="mr-5">
          <div>{{$t('profile.logOut')}}</div>
        </div>
    </div>
    </transition>
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
      ],
      windowWidth: window.innerWidth,
      dialog: false
    }
  },
  computed: {
    user() {
      return this.$store.getters.user
    }
  },
  methods: {
    forceReload(url) {
      this.dialog = false
      if (this.$route.path === url) {
        window.location.reload()
      }
    },
    logout() {
      this.$store.dispatch('logOut')
    },
  },
  mounted() {
    this.interval = setInterval(async() => {
      if (this.user) {
        await this.$store.dispatch('fetchBalance')
      }
    }, 10000)
    this.$nextTick(() => {
      window.addEventListener('resize', () => {
        this.windowWidth = window.innerWidth
      })
    })
  },
  beforeDestroy() {
    clearInterval(this.interval)
  },
}
</script>

<style lang="scss">
.navbar-margin {
  margin-left: auto;
}
.block {
  display: block;
}

.margin-zero:last-child {
  margin-top: 0;
}

[alt="cash"], [alt="exit"], [alt="account"], [alt="earth"] {
 width: 18px;
}


.header {
  height: 70px;
  width: 100%;
  background-color: $white;
  box-shadow: 0px 2px 7px rgba(0, 0, 0, 0.15);

  &__container {
    position: relative;
    z-index: 499;
    max-width: 1230px;
    width: 100%;
    margin: auto;
    height: inherit;
    display: flex;
    align-items: center;
    padding-right: 20px;
    padding-left: 20px;
    background-color: white;
  }

  &__nav {
    @media (max-width: 916px) {
      display: none;
    }
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
    @media (max-width: 916px) {
      display: none;
    }
  }

  &__action {
    @include reset-link;

    font-family: 'Roboto';
    font-style: normal;
    font-weight: normal;
    font-size: 14px;
  }

  &__user {
    display: flex;
    align-items: center;
  }
  .block {
    display: block;
  }

  &__balance {
    margin-right: 60px;
    position: relative;

    span {
      margin-right: 5px;
    }
  }

  &__lang {
    margin-left: 50px;
    @media (max-width: 916px) {
      display: none;
    }
  }

  .dialog-enter-active, .dialog-leave-active {
    transition: all 0.5s;
  }

  .dialog-enter, .dialog-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
    transform:translateY(-100%);
  }


  &__dialog {
    position: relative;
    z-index: 400;
    background-color: #f8f8f8;
    padding: 20px;
    .nav {
      .nav {
        margin-bottom: 30px;
        a {
          display: block;
          margin-bottom: 15px;
        }
      }
    }
  }
}
@media (max-width: 916px) {
  .navbar-toggle-active {
    background-color: #ddd !important;
  }
  .navbar-toggle {
    position: relative;
    float: right;
    padding: 9px 10px;
    margin-top: 8px;
    margin-bottom: 8px;
    background-color: transparent;
    background-image: none;
    border: 1px solid #ddd;
    border-radius: 4px;
    .icon-bar {
      display: block;
      width: 22px;
      height: 2px;
      border-radius: 1px;
      background-color: #888;
      margin-top: 4px;
    }
    .icon-bar:first-child {
      margin-top: 0;
    }
  }
}
</style>
