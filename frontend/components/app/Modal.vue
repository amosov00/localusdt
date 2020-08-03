<template>
  <transition name="fade">
  <div class="modal-wrapper">
    <div class="modal"></div>
  </div>
  </transition>
</template>

<script>
export default {

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
  backdrop-filter: blur(5px);
  z-index: 1000;
  .modal {
    height: 200px;
    width: 400px;
    background-color: $orange;
  }
}
</style>