<template>
	<footer class="footer">
		<div class="footer__container">
			<nuxt-link to="/">
				<img class="footer__logo" src="~/assets/icons/logo.svg" alt="Logo" />
			</nuxt-link>
			<nav class="footer__nav">
				<ul class="nav">
					<nuxt-link v-for="link in footerLinks" :key="link.title" :to="link.url" class="nav__item">{{link.title}}</nuxt-link>
				</ul>
			</nav>
      <p class="footer__copyright">Все права защищены © 2019 / 2020</p>
		</div>
	</footer>
</template>

<script>
export default {
  data() {
    return {
      footerLinks: [
        {title: 'Помощь', url: '/'},
        {title: 'О нас', url: '/'},
        {title: 'Как провести сделку', url: '/'},
        {title: 'Обратиться в службу поддержки', url: '/'},
      ]
    }
  },
}
</script>

<style lang="scss">
.footer {
	height: 75px;
	width: 100%;
	border-top: 1px solid rgba(17, 23, 29, 0.2);

	&__container {
		max-width: 1230px;
    width: 100%;
    padding-right: 20px;
    padding-left: 20px;
		height: inherit;
		margin: auto;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	&__nav {
		.nav {
			display: flex;
			align-items: center;
			height: 100%;
			&__item {
				margin-left: 40px;
        list-style: none;
        opacity: 0.5;
        transition: $interaction-transition;
        &:hover {
          opacity: 1;
        }
			}
		}
	}

	&__copyright {
		opacity: 0.5;
	}
}
</style>
