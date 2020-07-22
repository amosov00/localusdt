<template lang="pug">
  div.tabs-container
    input.tab-input(type="radio" name="tabs" id="tab-1")
    input.tab-input(type="radio" name="tabs" id="tab-2")
    label.tab.tab-1(for="tab-1" ref="tab1" @click="tabClick(1)") Tab 1
    label.tab.tab-2(for="tab-2" ref="tab2" @click="tabClick(2)") Tab 2
    div.content.content-1(ref="content1") content-1
    div.content.content-2(ref="content2") content-2
</template>

<script>
export default {
  data() {
    return {
      
    }
  },
  methods: {
    tabClick(id) {
      console.log(this.$refs.tab[id].classList)
      // this.$refs.tab1.classList.add('content--active')
    }
  },
};
</script>

<style lang="scss">
.tabs-container {
  background-color: $grey-light;
  width: 100%;
  height: 200px;
  display: flex;
  flex-wrap: wrap;
  position: relative;

  // #tab-1:checked ~ .tab-1 {
  //   background-color: lavender;
  // }
  // #tab-1:checked ~ .content-1 {
  //   display: block;
  // }

  // #tab-2:checked ~ .tab-2 {
  //   background-color: lavender;
  // }
  // #tab-2:checked ~ .content-2 {
  //   display: block;
  // }

  .content {
    width: 100%;
    display: none;
    padding: 20px;
    background-color: lavender;

    &--active {
      display: block;
    }
  }

  .tab-input {
    opacity: 0;
    position: absolute;
    top: 0;
    left: 0;
  }

  .tab {
    text-align: center;
    padding: 20px;
    flex-basis: 50%;
  }
}
</style>
