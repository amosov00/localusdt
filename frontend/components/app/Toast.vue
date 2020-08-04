<template>
<transition name="fade">
  <div class="toast" v-if="show" :class="{ 'red--bg': red, 'green--bg': green }">
    <h2 class="toast__title">{{ message }}</h2>
  </div>
</transition>
</template>

<script>
export default {
  data() {
    return {
      show: false,
      message: '',
      red: false,
      green: true
    }
  },
  methods: {
    halfLife() {
      setTimeout(() => {
        this.show = false
      }, 10000)
    }
  },
  created() {
    this.$store.subscribe((mutation, state) => {
      if (mutation.type === 'toast/showMessage') {
        this.message = state.toast.content
        this.red = state.toast.red
        this.green = state.toast.green
        this.show = true
        this.halfLife()
      }
    })
  }
}
</script>

<style lang="scss">
.toast {
  width: 100vw;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: sticky;
  top: 0;

  &__title {
    font-style: normal;
    font-weight: normal;
    font-size: 16px;
    color: $white;
  }
}
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
