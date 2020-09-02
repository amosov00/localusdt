<template lang="pug">
  div.textarea-box
    p.textarea-box__header {{header}}
    textarea.textarea(:value="value" @input="$emit('input', $event.target.value)"  :placeholder="placeholder")
</template>

<script>
export default {
  props: {
    value: String,
    placeholder: {
      type: String,
      default: '',
      require: false
    },
    header: {
      type: String,
      default: ''
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
    background-color: #f8f8f8;
    opacity: 0.8;
    border: 1px solid transparent;
    outline: none;
    border-radius: $border-radius;
    padding: 20px;
    width: 475px;
    max-width: 475px;
    min-width: 100%;
    min-height: 175px;
    max-height: 500px;
    height: 175px;

    &:focus {
      //box-shadow: $box-shadow;
      border: 1px solid #c8c8c8;
      caret-color: $orange;
    }
  }
}
</style>
