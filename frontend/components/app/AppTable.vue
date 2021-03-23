<template>
  <div :class="{'mb-80': pagination ? pagination : false}">
    <table class="table" :style="'max-width:'+ maxWidth">
      <thead class="table__head">
        <tr class="table__row">
          <th class="table__header" style="font-size: 10px;" v-for="(header, i) in headers" :key="i">{{ header }}</th>
        </tr>
      </thead>
      <tbody class="table__body">
        <template v-for="(item, i) in whichTable">
          <div class="table__trheader" v-if="walletTX && windowWidth < 1100" @click="switchTR(item)">
            <div>
              {{item.amount_usdt}} USDT
            </div>
            <div class="text--grey">
              <span v-if="item.type === 1">{{$t('profile.buyUSDT')}}</span>
              <span v-else-if="item.type === 2">{{$t('profile.sellUSDT')}}</span>
              {{regularDate(item.date)}}
            </div>
            <div class="table__indicator" :class="{
              'table__indicator--up': item.visible,
              'table__indicator--down': !item.visible,
            }"></div>
          </div>
          <tr
            class="table__row"
            v-if="item.visible || (windowWidth > 1100) || !walletTX"
            :data-item="i"
            :key="i"
          >
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
           <!-- v-show="pagesCount > 40 ?  i > 3 && i < 43 ? false : true : false " -->
          <button class="pagination__page-button" v-show="pagesCount > 10 ?  i > 3 && i < pagesCount - 3 ? false : true : false " v-for="(page, i) in pagesCount" :key="page" @click="goToPage(page)" :class="{'orange': currentPage === page}">{{page}}</button>
        </p>
        <button class="pagination__arrow-button" @click="nextPage">
          <InlineSvg class="pagination__arrow-icon" :src="require('~/assets/icons/arrow-right.svg')" />
        </button>
      </div>
      <div class="pagination__quantity" :class="{'pagination__quantity-mobile': windowWidth < 716}">
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
import formatDate from "@/mixins/formatDate";
export default {
  name:'AppTable',
  props: {
    incomingData: Array,
    headers: Array,
    pagination: {
      type: Boolean,
      default: false
    },
    maxWidth:{
      default:'1230px'
    },
    propsContPage:{
      default:15,
    },
    walletTX: {
      type: Boolean,
      default: false
    }
  },
  mixins: [formatCurreny, paymentMethod, formatDate],
  components: {
    Button,
    InlineSvg,
  },
  data() {
    return {
      currentPage: 1,
      contentPerPage: this.propsContPage,
      windowWidth: window.innerWidth,
      data: this.incomingData
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
      if(this.data !== null){
        return this.data.slice(
        this.currentPage * this.contentPerPage - this.contentPerPage,
        this.currentPage * this.contentPerPage
      )
      }
    },
    pagesCount() {
      if(this.data !== null){
        return Math.ceil(this.data.length / this.contentPerPage)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', () => {
        this.windowWidth = window.innerWidth
      })
    })
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
      this.currentPage = page;
    },
    switchTR(item) {
      const globalIndex = this.data.indexOf(item)
      this.data[globalIndex].visible = !this.data[globalIndex].visible;
    }
  },
  created() {
    this.$parent.$on('clickPageOne', this.goToPage);
  }
}
</script>

<style lang="scss" scoped>
.none-class {
  display: none;
}
.none-class .table__data:not(:last-child) {
  border-right: 0 solid #808080;
}

.table {
  border-collapse: collapse;
  margin: 25px 0;
  text-align: center;
  overflow-wrap:break-word;
  &__head {
    .table__row {
      word-wrap: break-word;
      color: #000;
      opacity: 0.3;
      font-weight: 500;
      text-transform: uppercase;
      text-align: left;
    }
  }

  &__indicator {
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    position: absolute;
    top: 50%;
    right: 5%;
    transform: translate(-50%, -50%);
  }

  &__indicator--up {
    border-bottom: 12px solid gray;
  }
  &__indicator--down {
    border-top: 12px solid gray;
  }

  &__header {
    padding: 20px;
    font-weight: 500;
    font-size: 16px;
  }
  &__body {
    .table__trheader {
      text-align: left !important;
      padding: 15px;
      border-radius: 5px;
      margin-top: 15px;
      border: 1px solid grey;
      position: relative;
      div:last-child {
        span:last-child {
          margin-right: 30px;
        }
      }
      div:first-child {
        font-size: 25px;
        margin-bottom: 8px;
      }
    }
    .table__row {
      overflow-wrap:break-word;
      word-wrap: break-word;
      line-height: 70px;
      @media (max-width: 1100px) {
        box-shadow: 0px 4px 15px 0px rgba(34, 60, 80, 0.2);
      }

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

  &__quantity-mobile {
    transform: translate(-50%, -50%);
    top: 50% !important;
    left: 50% !important;
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
