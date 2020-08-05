<template>
  <div class="tab" :style="{'top': `${top}px`}">
    <nav class="tab-nav">
      <div
        class="tab-nav__item"
        :class="{ 'tab-nav__item--active': firstTab }"
        @click="selectTab"
      >
        Быстрая покупка
      </div>
      <div
        class="tab-nav__item"
        :class="{ 'tab-nav__item--active': secondTab }"
        @click="selectTab"
      >
        Быстрая продажа
      </div>
    </nav>
    <div class="tab-body">
      <Input type="number" header="Цена за токен" placeholder="0,00" />
      <Input type="number" placeholder="0,00" />
      <Select :width="80" :options="currencyOptions" />
      <Select :width="370" :options="paymentOptions" />
      <Button green>Найти</Button>
    </div>
  </div>
</template>

<script>
import Input from '~/components/app/Input'
import Select from '~/components/app/Select'
import Button from '~/components/app/Button'
export default {
  props: {
    top: Number
  },
  components: {
    Input,
    Select,
    Button
  },
  data() {
    return {
      firstTab: true,
      secondTab: false,
      currencyOptions: [
        { name: 'RUB', value: 1 },
        { name: 'USD', value: 2 },
        { name: 'EUR', value: 3 }
      ],
      paymentOptions: [
        { name: 'Банковский перевод: Сбербанк', value: 1 },
        { name: 'Банковский перевод: Тиньков', value: 2 },
        { name: 'Свой вариант', value: 3 }
      ]
    }
  },
  methods: {
    selectTab() {
      if(this.firstTab) {
        this.secondTab = true
        this.firstTab = false
      } else {
        this.secondTab = false
        this.firstTab = true
      }
    }
  }
}
</script>

<style lang="scss">
.tab {
  position: absolute;
  top: 100px;
  right: 0;
  width: 100%;
  margin-top: 50px;
  margin-bottom: 50px;

  .tab-nav {
    display: flex;
    justify-content: center;
    @include montserrat;

    &__item {
      padding: 25px;
      cursor: pointer;
      border: 1px solid transparent;
      border-radius: 6px 6px 0px 0px;
      opacity: 0.5;

      &:first-child {
        margin-right: 30px;
      }

      &--active {
        border: 1px solid #f3f3f3;
        border-bottom: none;
        background-color: #fdfdfd;
        opacity: 1;
      }
    }
  }

  .tab-body {
    background-color: #fdfdfd;
    border: 1px solid #f3f3f3;
    height: 150px;
    margin-top: -1px;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    padding-bottom: 40px;

    & > * {
      margin-left: 25px;
      &:last-child {
        margin-left: 70px;
      }
    }
  }
}
</style>
