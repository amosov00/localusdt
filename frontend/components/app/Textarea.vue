<template lang="pug">
  div.textarea-box
    p.textarea-box__header {{header}}
    textarea.textarea(@input="updateValue($event.target.value)" :value="value" :placeholder="placeholder")
</template>

<script>
export default {
  props: {
    placeholder: {
      type: String,
      default: '',
      require: false
    },
    header: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      value: ''
    }
  },
  methods: {
    updateValue(value) {
      this.$emit('input', value)
    }
  }
}
</script>

<style lang="scss">
.textarea-box {
  &__header {
    font-size: 12px;
    opacity: 0.7;
    margin-left: 2px;
    margin-bottom: 5px;
  }

  .textarea {
    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 500;
    font-size: 12px;
    background-color: #f6f6f6;
    opacity: 0.8;
    background-color: $grey-light;
    border: 1px solid transparent;
    outline: none;
    border-radius: $border-radius;
    padding: 20px;
    transition: $interaction-transition;
    width: 475px;
    height: 175px;

    &:focus {
      box-shadow: $box-shadow;
      border: 1px solid #c8c8c8;
      caret-color: $orange;
    }
  }
}
</style>
