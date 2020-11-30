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
    halfLife(timeout) {
      setTimeout(() => {
        this.show = false
        this.$toast.closeToast()
      }, timeout)
    }
  },
  created() {
    this.$store.subscribe((mutation, { toast }) => {
      if (mutation.type === 'toast/showMessage') {
        const { content, red, green, timeout } = toast
        this.$toast.openToast()
        this.message = content
        this.red = red
        this.green = green
        this.show = true

        this.halfLife(timeout)
      }
    })
  }
}
</script>

<style lang="scss" scoped>
.toast {
  width: 100vw;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: sticky;
  top: 0;
  z-index: 1000000;
  max-width: 100%;

  &__title {
    font-style: normal;
    font-weight: normal;
    font-size: 16px;
    color: $white;
  }
}
.fade-enter-active, .fade-leave-active {
  transition: all .5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
  transform: scaleY(-1);
  height: 0;
}
</style>
