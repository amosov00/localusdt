<template>
  <div class="select" @click.stop="areOptionsVisible = !areOptionsVisible" :style="{width: `${width}px`}">
    <p class="select__header" v-if="header">{{header}}</p>
    <div class="select__body">
      <div class="select__selected">
        <p class="select__title">{{ selected.name }}</p>
        <span class="select__icon">
          <img src="~/assets/icons/arrow-down.svg" alt="" />
        </span>
      </div>
      <div class="select__options" v-if="areOptionsVisible">
        <p
          class="select__option"
          v-for="(option, i) in filteredOptions"
          :key="i"
          @click.stop="selectOption(option)"
        >
          {{ option.name }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import InlineSvg from 'vue-inline-svg'
export default {
  components: { InlineSvg },
  props: {
    options: {
      default() {
        return []
      }
    },
    selectedOptionProp: String,
    header: String,
    width: Number
  },
  data() {
    return {
      areOptionsVisible: false,
      selected: this.options[0]
    }
  },
  computed: {
    filteredOptions() {
      return this.options.filter(option => {
        return option.name !== this.selected.name
      })
    },
    selectedOption() {
      return this.options.find(el => el.value == this.selectedOptionProp) || this.options[0]
      // get: function() {
      // },
      // set: function(value) {
      //   this.selectedOption = value
      // }
    }
  },
  methods: {
    selectOption(option) {
      this.selected = option
      this.areOptionsVisible = false
      this.$emit('input', option.value)
    },
    hideSelect() {
      this.areOptionsVisible = false
    }
  },
  mounted() {
    document.addEventListener('click', this.hideSelect.bind(this), true)
  },
  beforeDestroy() {
    document.removeEventListener('click', this.hideSelect)
  }
}
</script>

<style lang="scss">
.select {
  @include montserrat;
  position: relative;
  z-index: 10000;
  &__header {
    font-size: 12px;
    opacity: 0.7;
    margin-left: 2px;
    margin-bottom: 5px;
  }

  &__body {
    background-color: $white;
    border: 1px solid #c8c8c8;
    border-radius: $border-radius;
    min-height: 50px;
    padding: 15px 10px;
    transition: $interaction-transition;
    cursor: pointer;

    &:hover {
      background-color: $grey-light;
    }
  }

  &__selected {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__title {
  }

  &__icon {
    display: inline-block;
  }

  &__options {
  }

  &__option {
    margin-top: 15px;
    opacity: .5;
    transition: $interaction-transition;

    &:hover {
      opacity: 1;
    }
  }
}
</style>
