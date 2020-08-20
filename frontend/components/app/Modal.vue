<template>
  <transition name="fade">
    <div class="modal-wrapper" v-show="show">
      <div class="modal">
        <h1 class="modal__title">Ваше объявление успешно размещено!</h1>
        <p class="modal__subtitle">
          Вы можете управлять им на странице покупки/продажи
        </p>
        <Button @click.native="hideModal" class="modal__button" green lg
          >Ок</Button
        >
      </div>
    </div>
  </transition>
</template>

<script>
import Button from '~/components/app/Button'
export default {
  props: {
    show: Boolean,
    type: {
      type: [String, Number]
    }
  },
  components: {
    Button
  },
  computed: {
    redirectPath() {
      switch (this.type) {
        case 2:
          return '/buy/'
          break
        case 1:
          return '/sell/'
          break
      }
    }
  },
  methods: {
    hideModal() {
      this.$emit('toggleModal', !this.show)
      this.$router.push(this.redirectPath)
    }
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

  .modal {
    text-align: center;

    &__subtitle {
      margin-top: 15px;
    }

    &__button {
      margin-top: 90px;
    }
  }
}
</style>
