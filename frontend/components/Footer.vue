<template lang="pug">
  footer.footer
    div.footer__container
      img.footer__logo(src="~/assets/icons/logo-grey.svg")
      p.paragraph-1.footer__copyright Все права защищены © 2019 / 2020
</template>

<script>
export default {}
</script>

<style lang="scss">
.footer {
  height: 75px;
  width: 100vw;
  border-top: 1px solid rgba(17, 23, 29, 0.2);

  &__container {
    max-width: 1240px;
    width: 100%;
    height: inherit;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__copyright {
    opacity: 0.5;
  }
}
</style>
