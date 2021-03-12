<template>
  <footer class="footer">
    <div class="footer__container">
      <nuxt-link to="/" class="footer__logowrapper">
        <img class="footer__logo" src="~/assets/icons/logo.svg" alt="Logo" />
      </nuxt-link>
      <nav class="footer__nav">
        <ul class="nav">
          <a
            v-for="link in footerLinks"
            :key="link.title"
            :href="link.url"
            class="nav__item"
          >
            {{link.title}}
          </a>
        </ul>
      </nav>
      <p class="footer__copyright">{{$t('footer.right')}} © 2019 / 2020</p>
    </div>
  </footer>
</template>

<script>
export default {
  data() {
    return {
      footerLinks: [
        { title: this.$t('footer.support'), url: '/' },
        { title: this.$t('footer.aboutUs'), url: '/' },
        { title: this.$t('footer.order'), url: '/' },
        { title: this.$t('footer.write'), url: this.$t('footer.writeUrl') },
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
    @media (max-width: 768px) {
      flex-direction: column;
      .footer__logowrapper {
        margin-right: auto;
        margin-top: 15px;
        margin-bottom: 15px;
      }
    }
  }

  &__nav {
    @media (max-width: 768px) {
      margin-right: auto;
    }
    .nav {
      display: flex;
      align-items: center;
      height: 100%;
      @media (max-width: 768px) {
        flex-direction: column;
        align-items: flex-start;
      }
      &__item {
        @media (max-width: 768px) {
          margin-top: 5px;
          margin-bottom: 5px;
          margin-left: 0;
        }
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
    @media (max-width: 768px) {
      margin-right: auto;
      margin-top: 15px;
      padding-bottom: 20px;
    }
  }
}
</style>
