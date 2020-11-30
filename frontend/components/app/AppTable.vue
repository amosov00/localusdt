<template>
  <div :class="{'mb-80': pagination ? pagination : false}">
    <table class="table">
      <thead class="table__head">
        <tr class="table__row">
          <th class="table__header" v-for="header in headers">{{ header }}</th>
        </tr>
      </thead>
      <tbody class="table__body">
        <template v-for="item in whichTable">
          <tr class="table__row">
            <slot :row="item" />
          </tr>
        </template>
      </tbody>
    </table>
    <div class="pagination" v-if="pagination">
      <div class="pagination__controller">
        <button class="pagination__arrow-button" @click="prevPage">
          <InlineSvg class="pagination__arrow-icon" :src="require('~/assets/icons/arrow-left.svg')" />
        </button>
        <p>
          <button class="pagination__page-button" v-for="page in pagesCount" :key="page" @click="goToPage(page)" :class="{'orange': currentPage === page}">{{page}}</button>
        </p>
        <button class="pagination__arrow-button" @click="nextPage">
          <InlineSvg class="pagination__arrow-icon" :src="require('~/assets/icons/arrow-right.svg')" />
        </button>
      </div>
      <div class="pagination__quantity">
        <button class="pagination__quantity-button" :class="{'black': contentPerPage === 15}" @click="setContentPerPage(15)"> 15 </button>
        <button class="pagination__quantity-button" :class="{'black': contentPerPage === 25}" @click="setContentPerPage(25)"> 25 </button>
        <button class="pagination__quantity-button" :class="{'black': contentPerPage === 50}" @click="setContentPerPage(50)"> 50 </button>
        <button class="pagination__quantity-button" :class="{'black': contentPerPage === 100}" @click="setContentPerPage(100)"> 100 </button>
      </div>
    </div>
  </div>
</template>

<script>
import InlineSvg from 'vue-inline-svg'
import Button from '~/components/app/Button'
import formatCurreny from '~/mixins/formatCurrency'
import paymentMethod from '~/mixins/paymentMethod'
export default {
  props: {
    data: Array,
    headers: Array,
    pagination: {
      type: Boolean,
      default: false
    }
  },
  mixins: [formatCurreny, paymentMethod],
  components: {
    Button,
    InlineSvg,
  },
  data() {
    return {
      currentPage: 1,
      contentPerPage: 15
    }
  },
  computed: {
    whichTable() {
      switch (this.pagination) {
        case true:
          return this.paginatedTableData
          break
        case false:
           return this.data
          break
        default:
          break
      }
    },
    paginatedTableData() {
      return this.data.slice(
        this.currentPage * this.contentPerPage - this.contentPerPage,
        this.currentPage * this.contentPerPage
      )
    },
    pagesCount() {
      return Math.ceil(this.data.length / this.contentPerPage)
    }
  },
  methods: {
    prevPage() {
      if (this.currentPage <= 1) {
        return
      }
      this.currentPage -= 1
    },
    nextPage() {
      if (this.paginatedTableData.length / this.contentPerPage < 1) {
        return
      }
      this.currentPage += 1
    },
    setContentPerPage(value) {
      this.contentPerPage = value
      this.currentPage = 1
    },
    goToPage(page) {
      this.currentPage = page
    }
  }
}
</script>

<style lang="scss" scoped>
.table {
  max-width: 1230px;
  width: 100%;
  border-collapse: collapse;
  margin: 25px 0;
  text-align: center;
  &__head {
    .table__row {
      color: #000;
      opacity: 0.3;
      font-weight: 500;
      text-transform: uppercase;
      text-align: left;
    }
  }

  &__header {
    padding: 20px;
    font-weight: 500;
    font-size: 16px;
  }
  &__body {
    .table__row {
      line-height: 70px;

      &:nth-child(2n) {
        background-color: #fdfdfd;
      }

      &:hover {
        background-color: #fdfdfd;
      }
    }
  }

  &__data {
    text-align: left;
    padding-left: 30px;
    font-weight: normal;

    .status {
      display: inline-block;
      height: 10px;
      width: 10px;
      border-radius: 50%;
      margin-left: 6px;
    }

    .orders-count {
      display: inline-block;
      margin-left: 15px;
      color: $grey-dark;
    }

    &:not(:last-child) {
      border-right: 1px solid $grey;
    }
  }
}
.pagination {
  max-width: 1230px;
  width: 100%;
  height: 20px;
  display: flex;
  justify-content: center;
  position: relative;

  &__controller {
    display: inline-block;
    max-width: 350px;
    width: 100%;
    height: 20px;
    display: flex;
    justify-content: space-between;
  }

  &__arrow-button {
    @include reset-button;
  }

  &__page-button {
    color: $grey-dark;
    @include reset-button;

    &:not(:last-child) {
      margin-right: 30px;
    }
  }

  &__quantity {
    position: absolute;
    top: 0;
    right: 0;
    display: inline-block;
    width: 122px;
    height: 20px;

    &:not(:last-child) {
      margin-right: 5px;
    }
  }

  &__quantity-button {
    @include reset-button;
    transition: $interaction-transition;
    color: $grey-dark;

    &:hover {
      color: $black;
    }

    &:not(:last-child) {
      margin-right: 10px;
    }
  }
}
</style>
