<template lang="pug">
  button(type="button" style="height: auto" :class="{'button--lg': lg, 'button--outlined': outlined, 'button--rounded': rounded, 'button--disabled': disabled, 'orange--bg': orange, 'green--bg': green, 'red--bg': red, 'button--white': white}" class="button" :disabled="disabled")
    slot
</template>

<script>
export default {
  props: {
    disabled: Boolean,
    rounded: {
      type: Boolean,
      default: false
    },
    lg: {
      type: Boolean,
      default: false
    },
    outlined: {
      type: Boolean,
      default: false
    },
    orange: {
      type: Boolean,
      default: false
    },
    green: {
      type: Boolean,
      default: false
    },
    red: {
      type: Boolean,
      default: false
    },
    white: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style lang="scss">
.button {
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 500;
  font-size: 16px;
  border: none;
  outline: none;
  border-radius: $border-radius;
  padding: 15px 30px;
  text-transform: uppercase;
  color: $white;
  cursor: pointer;
  transition: $interaction-transition;

  &:hover {
    transform: translateY(-2px);
    box-shadow: $box-shadow;
  }
  &:active {
    transform: translateY(0);
    box-shadow: none;
  }

  &--outlined {
    padding: 10px 30px;
    background-color: inherit;
    border: 1px solid $green;
    color: $green;
    &:hover {
      background-color: $green;
      color: $white;
      box-shadow: 0px 7px 17px rgba(72, 177, 144, 0.5),
        0px 2px 7px rgba(72, 177, 144, 0.3);
    }
  }
  &--rounded {
    border-radius: 50px;
  }

  &--disabled {
    background-color: #11171d;
    opacity: 0.2;

    &:hover {
      transform: translateY(0);
      box-shadow: none;
    }
  }

  &--lg {
    height: 50px;
    padding: 15px 50px;
  }
  &--white {
    border: 1px solid #888B8E;
    background-color: $white;
    font-style: normal;
    font-weight: 600;
    text-align: center;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #11171D;
  }
}
</style>
