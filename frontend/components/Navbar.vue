<template>
	<header class="header">
		<div class="header__container">
			<nuxt-link to="/">
				<img class="header__logo" src="~/assets/icons/logo.svg" alt="Logo" />
			</nuxt-link>
			<nav class="header__nav">
				<ul class="nav">
					<nuxt-link v-for="link in footerLinks" :key="link.title" :to="link.url" class="nav__item">{{link.title}}</nuxt-link>
				</ul>
			</nav>
			<div class="header__actions">
				<div v-if="!$userIsLoggedIn()">
          <nuxt-link class="header__action disabled" to="/signup"
            >Регистрация</nuxt-link
          >
          <nuxt-link class="header__action" to="/login">Вход</nuxt-link>
				</div>
        <div class="header__user" v-else>
          <p class="header__balance"><span class="grey-dark">Баланс:</span>{{user.balance_usdt}} USDT</p>
          <nuxt-link class="header__action" to="/profile">{{user.username}}</nuxt-link>
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
export default {
  components: {
    LangSwitcher
  },
	data() {
		return {
			footerLinks: [
				{title: 'Купить Tether', url: '/bid/buy'},
				{title: 'Продать Tether', url: '/bid/sell'},
			]
		}
  },
  computed: {
    user() {
      return this.$store.getters.user
    }
  },
}
</script>

<style lang="scss">
.header {
	height: 70px;
	width: 100vw;
	background-color: $white;
	box-shadow: 0px 2px 7px rgba(0, 0, 0, 0.15);

	&__container {
		max-width: 1170px;
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
