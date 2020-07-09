<template>
  <header class="header">
    <div class="header__container">
      <nuxt-link to="/">
        <img class="header__logo" src="~/assets/icons/logo.svg" alt="Logo" />
      </nuxt-link>
      <nav class="header__nav">
        <ul class="nav">
          <nuxt-link class="nav__item" to="/">Купить Tether</nuxt-link>
          <nuxt-link class="nav__item" to="/">Продать Tether</nuxt-link>
          <nuxt-link class="nav__item" to="/bid"
            >Разместить объявление</nuxt-link
          >
        </ul>
      </nav>
      <div class="header__actions">
        <nuxt-link class="header__action disabled" to="/signup"
          >Регистрация</nuxt-link
        >
        <nuxt-link class="header__action" to="/login">Вход</nuxt-link>
      </div>
    </div>
  </header>
</template>

<script>
export default {}
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
  }

  &__nav {
    .nav {
      display: flex;
      align-items: center;
      height: 100%;
      &__item {
        @include reset-link;

        font-family: 'Roboto', sans-serif;
        font-style: normal;
        font-weight: normal;
        font-size: 14px;
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
}
</style>
