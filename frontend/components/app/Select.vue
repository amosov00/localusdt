<template>
  <div class="select" :class="{'select--active': areOptionsVisible}">
    <div class="select__title" @click="areOptionsVisible = !areOptionsVisible">
      {{ selected }}
      <InlineSvg :class="{'select__arrow--active': areOptionsVisible}" :src="require('../../assets/icons/arrow-down.svg')" />
    </div>
    <div class="select__options" v-if="areOptionsVisible">
      <p
        v-for="option in options"
        :key="option.value"
        @click="selectOption(option)"
      >
        {{ option.name }}
      </p>
    </div>
  </div>
</template>

<script>
import InlineSvg from "vue-inline-svg";
export default {
  components: { InlineSvg },
  props: {
    options: {
      default() {
        return [];
      }
    },
    selected: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      areOptionsVisible: false
    };
  },
  methods: {
    selectOption(option) {
      this.$emit("select", option);
    },
    hideSelect() {
      this.areOptionsVisible = false;
    }
  },
  mounted() {
    document.addEventListener("click", this.hideSelect.bind(this), true);
  },
  beforeDestroy() {
    document.removeEventListener("click", this.hideSelect);
  }
};
</script>

<style lang="scss">
.select {
  position: relative;
  padding: 15px 10px;
  text-align: center;
  background: #ffffff;
  border: 1px solid #c8c8c8;
  border-radius: 6px;
  width: 100px;
  cursor: pointer;
  z-index: 100;
  transition: $interaction-transition;

  &--active {
    background-color: $grey-light;
  }

  &__options {
    margin-top: 5px;
    // position: absolute;
  }

  &__arrow--active {
    transform: rotate(180deg);
  }
}
</style>
