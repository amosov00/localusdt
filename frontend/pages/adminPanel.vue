<template>
  <div>
      <Tabs>
            <tab name="Пользователи" :selected="true">
                <Content v-if="users" title="Сделки" type="users" :dataInvoices="users" :headers="headersUsers">
                    <template slot-scope="{ data }">
                        <td class="table__data paddingSmall ">
                            <p>{{ data.username }}</p>
                        </td>
                        <td class="table__data paddingSmall ">
                            <p>
                                {{ data.email }}
                            </p>
                        </td>
                        <td class="table__data paddingSmall ">
                            <p>
                                {{ data.eth_address }} 
                            </p>
                        </td>
                        <td class="table__data paddingSmall ">
                        {{ data.balance_usdt }} 
                        </td>
                        <td class="table__data paddingNull" style="text-align:center;">
                            test    
                        </td>
                        <td class="table__data paddingNull" style="text-align:center;">
                            test
                        </td>
                        <td class="table__data paddingSmall" style="text-align:center; padding-right:10px;">
                             <Select
                                :v-model="data.is_active ? 'Активный': 'Неактивный'"
                                :width="120"
                                :options="selctOptions"
                                noCurrency
                                status
                                :user="data._id"
                                :hideArrow="true"
                                :selectedOptionProp="bannedOrActive(data.is_active, data.banned)"
                            />
                        </td>
                    </template>
                </Content>
            </tab>
            <tab name="Сделки" >
                <Content :key="componentInvoice" v-if="invoiceBoolean" title="Сделки" type="deal" :dataInvoices="dataInvoice" :headers="headersInvoice">
                    <template slot-scope="{ data }">
                        <td class="table__data paddingSmall ">
                            <p>{{ formatDate(data.finished_at) }}</p>
                            <p style="font-size:10px; padding:0; line-height:15px;">ID сделки: {{data._id}}</p>
                        </td>
                        <td class="table__data paddingSmall ">
                            <p>
                                {{ data.buyer_nickname }} - {{ data.seller_nickname }}
                            </p>
                        </td>
                        <td class="table__data paddingSmall ">
                            <p>
                                {{ data.amount_usdt }} - USDT
                            </p>
                        </td>
                        <td class="table__data paddingSmall ">
                        {{ data.status }} 
                        </td>
                        <td  class="table__data paddingNull" style="text-align:center;">
                            <Button :disabled="data.status !== 'waiting_for_tokens'" @click.native="freeze(data._id)" style="border-radius:50%; padding:0; height:40px;width:40px; margin-top:10px; " rounded outlined green></Button>
                        </td>
                        <td class="table__data paddingNull" style="text-align:center;">
                            <Button :disabled="data.status == 'cancelled'" @click.native="rollback(data._id)" style="border-radius:50%; padding:0; height:40px;width:40px; margin-top:10px; " rounded outlined green></Button>
                        </td>
                        <td class="table__data paddingNull" style="text-align:center;">
                            <Button @click.native="confirm(data._id)" style="border-radius:50%; padding:0; height:40px;width:40px; margin-top:10px; " rounded outlined green></Button>
                        </td>
                    </template>
                </Content>
            </tab>
      </Tabs>
      <!-- 30 минут -->
  </div>
</template>

<script>
import Tabs from '../components/tabsAdminPanel/Tabs'
import Tab from '../components/tabsAdminPanel/Tab'
import Content from '../components/AdminPanel/Content'
import Button from '@/components/app/Button'
import Input from '@/components/app/Input'
import Select from '@/components/app/Select'
import paymentMethod from '~/mixins/paymentMethod'
import formatDate from '~/mixins/formatDate'
export default {
    mixins: [paymentMethod, formatDate],
    data(){
        return{
            headersInvoice: [
                'Дата, время',
                'Стороны сделки',
                'Сумма',
                'Статус',
                'Заморозить',
                'Сбросить',
                'Отправить принудительно',
            ],
            headersUsers: [
                'Имя пользователя',
                'Эл. почта',
                'Адрес кошелька',
                'Баланс USDT',
                'Баланс пользв кошельков',
                'Баланс ЕТН',
                'Статус',
            ],
            selctOptions:[
                { name: 'Активный', value: 1 },
                { name: 'Заморожен', value: 2 },
                { name: 'Заблокирован', value: 3 },
            ],
            dataInvoice:null,
            invoiceBoolean:false,
            componentInvoice:1
        }
    },
    components:{
        Tabs,
        Tab,
        Content,
        Button,
        Input,
        Select
    },
    methods:{
        async freeze(id){
            let res = await this.$axios.put(`/admin/invoice/${id}/freeze/`);
            if(res.status == 200){
                this.invoiceBoolean = false
                // this.dataInvoice = this.dataInvoice.filter(e => e._id !== id)
                // let data = this.dataInvoice
                //     data.forEach(e=>{
                //    if( e._id == id){
                //        e.status = 'lol'
                //    }
                // })
                // this.dataInvoice = data
                setTimeout(() => {
                    this.componentInvoice++
                    this.invoiceBoolean = true
                }, 1000);
            }
        },
        async rollback(id){
            try{
                let res = await this.$axios.put(`/admin/invoice/${id}/rollback/`)
                console.log(res);

            }catch(e){
                console.log(e);
            }
        },
        async cancel(){
            try{
                let res = await this.$axios.put(`/admin/invoice/${id}/cancel/`)
                console.log(res);

            }catch(e){
                console.log(e);
            }
        },  
        async confirm(id){
                let res = await this.$axios.put(`/admin/invoice/${id}/confirm/`)
                .catch(()=>{
                    this.invoiceBoolean = false
                    this.$store.dispatch('adminPanel/getInvoices')
                    .then(()=>{
                        this.dataInvoice = this.$store.getters['adminPanel/getInvoices']
                        this.invoiceBoolean = true
                        this.componentInvoice++
                    })
                })
                

        },
        bannedOrActive(e,y){
            let res;
            if(y == false){
                res = 1
            }
            if(y == true){
                res = 3
            }

            if(e == true){
                res =  1
            }
            if(e == false){
                res =  2
            }
            return res
        }
    },
    computed:{
      invoices() {
        return this.$store.getters['adminPanel/getInvoices']
      },
      users() {
        return this.$store.getters['adminPanel/getUsers']
      },
    },
    async created() {
        this.$store.dispatch('adminPanel/getInvoices')
        .then(()=>{
            this.dataInvoice = this.$store.getters['adminPanel/getInvoices']
            this.invoiceBoolean = true
        })
        this.$store.dispatch('adminPanel/getUsers')
    },
}
</script>
<style lang="scss" scoped>
    .adminPanel__wrapper{
        width: 100%;
        padding-top: 100px;
    }
    .adminPanel__seachPanel{
        margin-left: 40px;
    }
    .adminPanel__title{
        width: 100vw;
        margin-bottom: 50px;
    }
    .adminPanel__wrapper_searchForm{
        display: flex;
        margin-bottom: 50px;
    }
    .paddingSmall{
        padding-left: 10px;
        line-height: 30px;
        font-size: 15px;
    }
    .paddingNull{
        padding-left: 0;
    }
    .table__data{
        max-width: 150px;
        overflow-wrap:break-word;
        word-wrap: break-word;
    }
</style>