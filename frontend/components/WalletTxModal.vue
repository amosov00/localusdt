<template>
  <transition name="fade">
    <div class="modal-wrapper" v-show="show">
      <div class="text-center">
        <h1>Транзакция обрабатывается</h1>
        <p class="mt-20">
          В зависимости от загрузки сети транзакции обрабатываются от 5 минут до
          суток
        </p>
        <Button
          @click.native="$emit('toggleModal', false)"
          class="referral__button"
          green
          lg
          >Ok</Button
        >
      </div>
    </div>
  </transition>
</template>

<script>
import Button from '~/components/app/Button'
export default {
  props: {
    show: Boolean
  },
  components: {
    Button
  }
}
</script>

<style lang="scss">
.modal-wrapper {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  -webkit-backdrop-filter: blur(40px);
  backdrop-filter: blur(40px);
  z-index: 100000000000000;
}
</style>
