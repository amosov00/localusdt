<template>
  <div class="input" :style="{width: `${width}px`}">
    <p class="input__header" v-if="header">{{ header }}</p>
    <div  class="input__body">
      <span class="input__icon" v-if="icon">
        <InlineSvg :src="require(`~/assets/icons/${icon}.svg`)" />
      </span>
      <input :class="{'input--disabled': disabled}" :disabled="disabled" class="input__field" :type="showPasswordField" :value="value" @input="$emit('input', $event.target.value)" :placeholder="placeholder" />
      <span class="input__icon" v-if="type === 'password'" @click="toggleShowPassword">
        <InlineSvg :src="require(`~/assets/icons/${passwordIcon}.svg`)" />
      </span>
      <span class="input__icon" v-else-if="endIcon" :style="{'cursor': endIcon === 'copy' ? 'pointer' : 'default'}" @click="copy">
        <InlineSvg :src="require(`~/assets/icons/${endIcon}.svg`)" />
      </span>
      <span
        class="input__icon"
        :style="{'cursor': endIcon === 'copy' ? 'pointer' : 'default'}"
        v-if="limitInput && windowWidth < 607"
      >
        USDT
      </span>
    </div>
    <div class="input__hints">
      <p v-if="hint" class="input__hint" v-html="$t('main.inputWarn')"></p>
      <p v-if="hintTwo" class="input__hintTwo">
        {{ typeCurrency == 2 ? $t('main.PriceSettingEquation2') : $t('main.PriceSettingEquation') }}
      </p>
    </div>
  </div>
</template>

<script>
import InlineSvg from 'vue-inline-svg'
export default {
  components: { InlineSvg },
  props: {
    value: {
      require: false
    },
    limitInput: {
      default: false,
      type: Boolean
    },
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
    typeCurrency:{
      type: [String, Number],
      default: 1,
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
    },
    hint: Boolean,
    hintTwo:Boolean,
    disabled: Boolean,
    toastText: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      showPassword: false,
      windowWidth: window.innerWidth
    }
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', () => {
        this.windowWidth = window.innerWidth
      })
    })
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
      this.showPassword = !this.showPassword
    },
    copy() {
      const text = this.toastText ? this.toastText : this.$t('main.addressCopied')
      this.$clipboard(this.value)
      this.$toast.showMessage({content: text, green: true})
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
  @media (max-width: 768px) {

  }

  &--disabled {
    cursor: not-allowed;
  }

  &__hint {
    @media (max-width: 846px) {
      position: static;
      margin-top: 15px;
    }
    position: absolute;
    top: 40%;
    left: 109%;
    width: 330px;
    font-style: italic;
    opacity: .5;
  }
  &__hintTwo{
    @media (max-width: 846px) {
        position: static;
        margin-top: 15px;
    }
    position: absolute;
    top: 0%;
    right: -70%;
    left:108%;
    font-style: italic;
    opacity: .5;
  }

  &__header {
    position: absolute;
    top: -20px;
    left: 2px;
    font-size: 12px;
    opacity: 0.7;
  }

  &__body {
    position: relative;
    display: flex;
    align-items: center;
    background-color: #eee;
    height: 51px;
    width: 100%;
    opacity: 0.8;
    background-color: $grey-light;
    border: 1px solid transparent;
    border-radius: $border-radius;
    transition: $interaction-transition;
    padding: 10px 20px;

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
