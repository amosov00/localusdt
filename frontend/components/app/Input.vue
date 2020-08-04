<template>
  <div class="input" :style="{width: `${width}px`}">
    <p class="input__header" v-if="header">{{ header }}</p>
    <div class="input__body">
      <span class="input__icon" v-if="icon">
        <InlineSvg :src="require(`~/assets/icons/${icon}.svg`)" />
      </span>
      <input class="input__field" :type="showPasswordField" @input="updateValue($event.target.value)" v-model="value" :value="value" :placeholder="placeholder" />
      <span class="input__icon" v-if="type === 'password'" @click="toggleShowPassword">
        <InlineSvg :src="require(`~/assets/icons/${passwordIcon}.svg`)" />
      </span>
      <span class="input__icon" v-else-if="endIcon">
        <InlineSvg :src="require(`~/assets/icons/${endIcon}.svg`)" />
      </span>
    </div>
  </div>
</template>

<script>
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
      default: '',
      required: false
    },
    endIcon: {
      type: String,
      default: '',
      required: false
    },
    header: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      showPassword: false,
      value: ''
    }
  },
  computed: {
    passwordIcon() {
      if (this.showPassword) {
        return 'eye'
      } else {
        return 'eye-off'
      }
    },
    showPasswordField() {
      if (this.type === 'password' && this.showPassword) {
        return 'text'
      } else {
        return this.type
      }
    }
  },
  methods: {
    toggleShowPassword() {
      console.log('click')
      this.showPassword = !this.showPassword
    },
    updateValue(value) {
      this.$emit('input', value)
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

  &__header {
    font-size: 12px;
    opacity: 0.7;
    margin-left: 2px;
    margin-bottom: 5px;
  }

  &__body {
    display: flex;
    align-items: center;
    background-color: #eee;
    height: 45px;
    width: 100%;
    opacity: 0.8;
    background-color: $grey-light;
    border: 1px solid transparent;
    border-radius: $border-radius;
    transition: $interaction-transition;
    padding: 10px;

    &:focus-within {
      border: 1px solid #c8c8c8;
      caret-color: $orange;

      box-shadow: 0px 8px 9px rgba(67, 78, 74, 0.07),
        0px 16px 23px rgba(67, 78, 74, 0.09);
    }
  }

  &__field {
    width: 100%;
    height: 100%;
    outline: none;
    border: none;
    background-color: inherit;

    &:focus {
      caret-color: $orange;
    }
  }

  &__icon {
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
