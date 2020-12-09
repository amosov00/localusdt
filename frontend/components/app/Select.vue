<template>
  <div class="select" :style="{width: `${width}px`}">
    <p class="select__header" v-if="header">{{header}}</p>
    <div class="select__body" @click.stop="toggle" :class="{ 'select__body--open': areOptionsVisible }">
      <div class="select__selected">
        <p class="select__title">{{ selected.name }}</p>
        <span class="select__icon" v-if="!hideArrow">
          <img src="~/assets/icons/arrow-down.svg" alt="" />
        </span>
      </div>
      <div class="select__options" v-if="areOptionsVisible" >
        <div
          class="select__option" style="z-index:99999;"
          v-for="(option, i) in filteredOptions"
          :key="i"
          @click.stop="selectOption(option)"
        >
          {{ option.name }}
        </div>
        
      </div>
    </div>
  </div>
</template>

<script>
import InlineSvg from 'vue-inline-svg'
export default {
  components: { InlineSvg },
  props: {
    selectedOptionProp: {
      type: [String, Number],
      default: 1
    },
    user:{
      type:[String, Number]
    },
    noCurrency: Boolean,
    status: Boolean,  
    options: {
      default() {
        return []
      }
    },
    header: String,
    width: Number,
    hideArrow: Boolean
  },
  data() {
    return {
      areOptionsVisible: false,
      selected:'',
      // selected: this.options[0]
    }
  },
  watch:{
    selectedOptionProp(){
      this.selected = this.options.find(option => option.value == (this.selectedOptionProp * 1))
    }
  },  
  computed: {
    filteredOptions() {
      return this.options.filter(option => {
        return option.name !== this.selected.name
      })
    },
    selectedComputed(){
     this.selected = this.options.find(option => option.value == (this.selectedOptionProp * 1))
    }
  },
  methods: {
    toggle() {
      this.areOptionsVisible = !this.areOptionsVisible
    },
    selectOption(option) {
      this.selected = option
      this.areOptionsVisible = false
      console.log(option);
      if(!this.noCurrency)  this.$store.dispatch('fetchCurrencyPrice', option.value)
      if(this.status && this.user) this.$store.dispatch('adminPanel/userStatus', {value: option.value, user:this.user})
      this.$emit('input', option.value)
    },
    hideSelect() {
      this.areOptionsVisible = false
    }
  },
  mounted() {
    document.addEventListener('click', this.hideSelect, { capture: false })
    this.selected = this.options.find(option => option.value == (this.selectedOptionProp * 1))
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
    cursor: pointer;
    user-select: none;
    position: relative;
    box-sizing: border-box;

    &--open {
      border-bottom-left-radius: 0;
      border-bottom-right-radius: 0;
      border-bottom: 0;
      box-shadow: 0 8px 9px rgba(67, 78, 74, 0.07), 0 16px 23px rgba(67, 78, 74, 0.09);
    }
  }

  &__selected {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 10px;
    transition: $interaction-transition;
    &:hover {
      background-color: $grey-light;
    }
  }

  &__title {
  }

  &__icon {
    display: inline-block;
  }

  &__options {
    position: absolute;
    background-color: #ffffff;
/*    width: calc(100% + 2px);
    left: -1px;*/
    z-index: 99999;
    width: calc(100% + 2px);
    left: -1px;
    box-sizing: border-box;
    border: 1px solid #c8c8c8;
    border-top: 0;
    border-radius: 0 0 $border-radius $border-radius;
    box-shadow: 0 8px 9px rgba(67, 78, 74, 0.07), 0 16px 23px rgba(67, 78, 74, 0.09);
  }

  &__option {
    padding: 15px 10px;
    opacity: .5;
    transition: $interaction-transition;

    &:hover {
      opacity: 1;
      background-color: $grey-light;
    }
  }
}
</style>
