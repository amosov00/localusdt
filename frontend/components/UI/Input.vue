<template lang="pug">
  div.input(:style="{width: `${width}px`}")
    div.input__box
      div.input__header(v-if="inputHeader") {{header}}
      input.input__field(:placeholder="placeholder" :type="showPasswordField" min="0")
      InlineSvg.input__icon(v-if="inputIcon" :src="require(`~/assets/icons/${icon}.svg`)")
      span.input__icon--end(v-if="inputEndIcon") {{endIcon}}
      InlineSvg.input__icon--eye(:src="require(`~/assets/icons/${passwordIcon}.svg`)" v-if="type === 'password'" @click="toggleShowPassword")
</template>

<script>
/* eslint-disable */
import InlineSvg from 'vue-inline-svg'
export default {
  components: { InlineSvg },
  props: {
    type: {
      type: String,
      default: 'text'
    },
    placeholder: {
      type: String,
      default: ''
    },
    width: {
      type: Number
    },
    icon: {
      type: String,
      required: false
    },
    endIcon: {
      type: String,
      required: false
    },
    header: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      showPassword: false
    }
  },
  computed: {
    passwordIcon() {
      if (this.showPassword) {
        return 'eye-off'
      } else {
        return 'eye'
      }
    },
    showPasswordField() {
      if (this.type === 'password' && this.showPassword) {
        return 'text'
      } else {
        return this.type
      }
    },
    inputIcon() {
      if (this.icon) {
        return true
      } else {
        return false
      }
    },
    inputEndIcon() {
      if (this.endIcon) {
        return true
      } else {
        return false
      }
    },
    inputHeader() {
      if (this.header) {
        return true
      } else {
        return false
      }
    }
  },
  methods: {
    toggleShowPassword() {
      this.showPassword = !this.showPassword
    }
  }
}
</script>

<style lang="scss">
.input {
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 500;
  font-size: 12px;
  position: relative;

  &__header {
    opacity: 0.7;
    margin-left: 2px;
    margin-bottom: 5px;
  }

  &__field {
    height: 45px;
    width: 100%;
    opacity: 0.8;
    background-color: $grey-light;
    border: 1px solid transparent;
    outline: none;
    border-radius: $border-radius;
    padding: 20px 45px;
    transition: $interaction-transition;

    &:focus {
      box-shadow: $box-shadow;
      border: 1px solid #c8c8c8;
      caret-color: $orange;
    }
  }

  &__icon {
    transform: translate(-50%, -50%);
    position: absolute;
    top: 50%;
    left: 25px;

    &--end {
      transform: translate(-50%, -50%);
      position: absolute;
      top: 70%;
      right: 10px;
      font-size: 16px;
      word-wrap: break-word;
      text-transform: uppercase;
      opacity: 0.5;
    }

    &--eye {
      cursor: pointer;
      transform: translate(-50%, -50%);
      position: absolute;
      top: 50%;
      right: 20px;
      opacity: 0.5;
    }
  }

  &__error {
    color: $red;
    // margin: 2px;
  }
}
</style>
