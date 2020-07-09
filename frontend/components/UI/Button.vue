<template lang="pug">
  button(type="button" :class="{'button--lg': lg, 'button--outlined': outlined, 'button--rounded': rounded, 'orange--bg': orange, 'green--bg': green, 'red--bg': red}" class="button")
    slot
</template>

<script>
export default {
  props: {
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
    }
  }
};
</script>

<style lang="scss">
.button {
  font-family: "Montserrat";
  font-style: normal;
  font-weight: 500;
  font-size: 16px;
  height: 45px;
  border: none;
  // outline: none;
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
    // height: 40px;
    // width: 140px;
    // padding: 10px 30px;
    // background-color: inherit;
    // border: 1px solid $green;
    // color: $green;
  }

  &--lg {
    height: 50px;
    padding: 15px 50px;
  }
}
</style>
