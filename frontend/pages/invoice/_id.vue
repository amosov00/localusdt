<template>
<section class="order">
    <header class="order__header">
    <h1 class="ad__title">{{$t('invoice.contact')}} № {{ invoice._id }}</h1>
    <div class="order__info">
        <div>
        <span class="opacity-50 fz-20">
            <span>{{ roleAction }}</span>
            <span>{{ commaSplitting(invoice.amount_usdt) }} USDT {{$t('invoice.for')}}</span>
            <span>{{ commaSplitting(invoice.amount) }} {{returnCurrency(invoice)}} </span>
        </span>
        <div class="ad__subtitle">
            <p>
            <span class="green">{{$t('invoice.status')}}</span>
            {{ invoiceStatus(invoice.status) }}
            </p>
            <p
            class="underline-link red"
            v-if="
                invoice.status === 'waiting_for_payment' && user._id === invoice.buyer_id ||
                invoice.status === 'waiting_for_tokens' && user._id === invoice.buyer_id
            "
            @click="cancelModal = true"
            >
            {{$t('invoice.cancel')}}
            </p>
        </div>
        </div>
        <div v-if="showTimer" class="order__timer">{{time}}</div>
    </div>
    </header>
    <OrderInfo :order="invoice" />
    <div class="order__footer">
    <Chat :invoice="invoice" :name="roleUser" />
    <SendMoneySteps v-if="role === 'seller'" :invoice="invoice" />
    <SendUSDTSteps v-else-if="role === 'bayer'" :invoice="invoice" />
    </div>
    <InvoiceCancelModal
    :show="cancelModal"
    @toggleModal="cancelModal = $event"
    :invoice="invoice"
    />
</section>
</template>

<script>
import { mapGetters } from 'vuex'
import formatCurrency from '~/mixins/formatCurrency'
import formatDate from '~/mixins/formatDate'
import invoiceStatuses from '~/mixins/invoiceStatuses'
import Button from '~/components/app/Button'
import OrderForm from '~/components/order/OrderForm'
import OrderInfo from '~/components/order/OrderInfo'
import Chat from '~/components/app/Chat'
import SendUSDTSteps from '~/components/invoice/SendUSDTSteps'
import SendMoneySteps from '~/components/invoice/SendMoneySteps'
import InvoiceCancelModal from '~/components/InvoiceCancelModal'
import moment from 'moment'

export default {
name: 'invoice_by_id',
mixins: [formatCurrency, invoiceStatuses, formatDate],
components: {
    Button,
    OrderForm,
    OrderInfo,
    Chat,
    SendUSDTSteps,
    SendMoneySteps,
    InvoiceCancelModal,
},
data() {
    return {
    cancelModal: false,
    invoiceId: this.$route.params.id,
    interval: null,
    timer: null,
    time: null
    }
},
computed: {
    ...mapGetters({
    invoice: 'invoice/invoiceById',
    user: 'user',
    }),
    roleAction() {
    if (
        (this.invoice.ads_type || this.invoice.type === 1) &&
        this.invoice.seller_username === this.user.username
    ) {
        return this.$t('invoice.sell')
    } else if (
        (this.invoice.ads_type || this.invoice.type === 2) &&
        this.invoice.buyer_username === this.user.username
    ) {
        return this.$t('invoice.buy')
    }
    },
    role() {
    if (
        (this.invoice.ads_type || this.invoice.type === 1) &&
        this.invoice.seller_username === this.user.username
    ) {
        return 'bayer'
    } else if (
        (this.invoice.ads_type || this.invoice.type === 2) &&
        this.invoice.buyer_username === this.user.username
    ) {
        return 'seller'
    }
    },
    roleUser() {
    switch (this.role) {
        case 'bayer':
        return this.invoice.buyer_username
        break
        case 'seller':
        return this.invoice.username || this.invoice.seller_username
        break
        default:
        break
    }
    },
    showTimer() {
    const { status } = this.invoice
    const statuses = ['waiting_for_tokens', 'waiting_for_payment']
    return statuses.includes(status)
    },
    timerDuration() {
    const { status } = this.invoice
    if (status === 'waiting_for_payment') {
        return 90
    }
    return status === 'waiting_for_tokens' ? 30 : 0
    }
},
created() {
    this.interval = setInterval(async() => {
        await this.$store.dispatch('invoice/fetchInvoiceById', this.invoiceId)
        if (this.invoice === 'waiting_for_tokens') {
            clearInterval(this.interval)
        }
    }, 10000)
},
mounted() {
    this.timer = setInterval(() => {
    this.checkTime()
    }, 1000)
},
methods: {
    returnCurrency(row){
    switch(row.currency){
        case 1:
        return '₽'
        break
        case 2:
        return 'Br'
        break
        case 3:
        return '$'
        break
        case 4:
        return '€'
        break
    }
    },
    checkTime() {
    this.diffDate(this.invoice.status_changed_at)
    },
    diffDate(date) {
    const timeOffset = moment().utcOffset()
    const startTime = moment(date)
        .add(this.timerDuration, 'minutes')
        .format('HH:mm:ss')
    const endTime = moment()
        .subtract(timeOffset, 'minutes')
        .format('HH:mm:ss')
    const seconds = moment(endTime, 'HH:mm:ss')
        .diff(moment(startTime, 'HH:mm:ss'), 'seconds')
    const duration = moment
        .duration(seconds, 'seconds')
    const time = `${duration.hours()}:${duration.minutes()}:${duration.seconds()}`
    this.time = moment(time, 'HH:mm:ss')
        .format('HH:mm:ss')
    }
},
beforeDestroy() {
    clearInterval(this.interval)
    clearInterval(this.timer)
},
asyncData({ route, store }) {
    return store.dispatch('invoice/fetchInvoiceById', route.params.id)
},
}
</script>

<style lang="scss">
.order {
margin-top: 50px;

&__timer {
    padding: 10px 30px;
    font-size: 30px;
}

&__title {
    display: inline-block;
}

&__subtitle {
    display: flex;
    justify-content: space-between;
}

&__payment-method {
    margin-top: 20px;
}

&__footer {
    margin-top: 30px;
    margin-bottom: 30px;
    display: flex;
    justify-content: space-between;
}

&__info {
    display: flex;
    justify-content: space-between;
}

.body {
    margin-top: 10px;
    height: 100%;
    // background-color: $orange;
    border-top: 1px solid $grey;
    border-bottom: 1px solid $grey;
    padding: 50px 0 50px 0;

    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;

    &__info {
    // background-color: $red;
    min-width: 200px;
    max-width: 450px;
    width: 100%;
    display: flex;
    flex-direction: column;

    .box {
        display: flex;
        justify-content: space-between;

        & > * {
        font-size: 14px;
        margin-bottom: 15px;
        }
    }
    }

    .condition {
    min-width: 350px;
    max-width: 500px;
    width: 100%;

    &__box {
        margin-top: 30px;
        background: rgba(72, 177, 144, 0.05);
        border-radius: $border-radius;
        padding: 30px 15px;
    }
    }
}
}
</style>
