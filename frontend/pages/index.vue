<template lang="pug">
  div
    NonAuthorizedHero
    section.table-section
      h1.table-section__title Купить USDT
      Table
      p.table-section__subtitle Показать больше объявлений
    section.table-section
      h1.table-section__title Продать USDT
      Table
      p.table-section__subtitle Показать больше объявлений
</template>

<script>
import NonAuthorizedHero from "~/components/NonAuthorizedHero";
import SellBuyTab from "~/components/SellBuyTab";
import Table from "~/components/app/Table";
import Select from "~/components/app/Select";
export default {
  components: { NonAuthorizedHero, SellBuyTab, Table, Select },
  data() {
    return {
      options: [
        { name: "RUB", value: "rub" },
        { name: "USD", value: "usd" },
        { name: "EUR", value: "eur" }
      ],
      selected: "Selected"
    };
  },
  methods: {
    selectedOption(option) {
      this.selected = option.name;
    }
  }
};
</script>

<style lang="scss">
.table-section {
  margin-top: 120px;
  margin-bottom: 120px;
  &__subtitle {
    margin-top: 30px;
    color: $orange;
    text-decoration: underline;
  }
}
</style>
