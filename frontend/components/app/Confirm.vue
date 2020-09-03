<template>
  <transition name="fade">
    <div class="modal-wrapper" v-show="show">
      <div class="modal">
        <h1 class="modal__title">{{ title }}</h1>
        <p class="modal__subtitle">
          {{ subtitle }}
        </p>
        <slot name="actions"/>
<!--        <Button @click.native="hideModal" class="modal__button" green lg>Ок</Button>
        <Button @click.native="hideModal" class="modal__button" green lg>Отмена</Button>-->
      </div>
    </div>
  </transition>
</template>

<script>
import Button from '~/components/app/Button'
export default {
  props: {
    title: String,
    subtitle: String,
    show: Boolean,
    type: {
      type: [String, Number]
    }
  },
  components: {
    Button
  },
  methods: {
    hideModal() {
      this.$emit('toggleModal', !this.show)
    }
  }
}
</script>

<style lang="scss" scoped>
.modal-wrapper {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 100000000;
  backdrop-filter: blur(20px);
  background-color: rgba(255, 255, 255, 0.1);

  .modal {
    text-align: center;

    &__title {
      margin-bottom: 90px;
    }

    &__subtitle {
      margin-top: 15px;
    }

    &__button {
      margin-top: 90px;
    }
  }
}
</style>
