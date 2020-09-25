<template>
  <div>
    <h2 class="fw-500 mt-50">История транзакций</h2>
    <AppTable class="mb-80" :data="transactions" :headers="headers" pagination>
      <template slot-scope="{ row }">
        <td class="table__data">
          {{regularDate(row.date)}}
        </td>
        <td class="table__data">{{ transactionEvent(row.event) }}</td>
        <td class="table__data">
            <span>
              {{ row.address }}
            </span>
            <a
              class="ml-15"
              :href="`https://etherscan.io/address/${row.address}`"
              target="_blank"
              rel="noopener noreferrer"
            >
              <InlineSvg :src="require('~/assets/icons/redirect.svg')" />
            </a>
          </td>
          <td class="table__data fw-500">
            {{ commaSplitting(row.amount_usdt) }} USDT
          </td>
          <td
            class="table__data"
            :style="{ color: statusColor(row.status) }"
          >
            {{ transactionStatus(row.status) }}
          </td>
      </template>
    </AppTable>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import formatDate from '~/mixins/formatDate'
import formatCurrency from '~/mixins/formatCurrency'
import AppTable from '~/components/app/AppTable'
import InlineSvg from 'vue-inline-svg'
export default {
  mixins: [formatDate, formatCurrency],
  components: {
    InlineSvg,
    AppTable
  },
  data() {
    return {
      headers: ['Дата', 'Действие', 'Адрес', 'Сумма', 'Статус']
    }
  },
  computed: {
    ...mapGetters({
      transactions: 'wallet/transactions'
    })
  },
  methods: {
    transactionStatus(status) {
      switch (status) {
        case 1:
          return 'Обрабатывается'
          break
        case 2:
          return 'Отменена'
          break
        case 3:
          return 'Выполнено'
          break
        default:
          break
      }
    },
    transactionEvent(event) {
      switch (event) {
        case 1:
          return 'Пополнение USDT'
          break
        case 2:
          return 'Вывод USDT'
          break
        default:
          break
      }
    },
    statusColor(status) {
      switch (this.transactionStatus(status)) {
        case 'Выполнено':
          return '#48B190'
          break
        case 'Обрабатывается':
          return '#ED9F43'
          break
        case 'Отменена':
          return '#B31B11'
          break
      }
    }
  }
}
</script>
