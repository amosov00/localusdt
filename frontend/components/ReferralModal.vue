<template>
  <transition name="fade">
  <div class="modal-wrapper" v-show="show">
    <div class="referral">
      <h1 class="referral__title">Условия реферальной программы</h1>
      <div class="referral__container">
      <p class="referral__condition">Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.Lorem ipsum dolor sit amet consectetur adipisicing elit. Deleniti minima, atque deserunt vitae pariatur delectus illo est, quibusdam culpa ut voluptatibus eos nihil corrupti rerum molestias quam odit sed at.</p>
      </div>
      <Button @click.native="hideModal" class="referral__button" green lg>Ок</Button>
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
  },
  methods: {
    hideModal() {
      this.$emit('toggleModal', !this.show)
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
  backdrop-filter: blur(40px);
  z-index: 100000000000000;

  .referral {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    &__title {
      font-weight: 500;
    }

    &__container {
      width: 500px;
      max-height: 300px;
      height: 100%;
      overflow: scroll;
      border-top: 1px solid #E7E8E8;
      margin-top: 70px;
    }

    &__condition {
    text-align: center;
      @include montserrat;
      overflow: scroll;
      font-size: 12px;
    }
    
    &__button {
      margin-top: 80px;
    }

  }
}
</style>