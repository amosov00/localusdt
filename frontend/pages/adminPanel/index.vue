<template>
  <div>
      <Tabs vertical>
            <tab name="Пользователи" :selected="true">
              <!-- tab USER -->
              <Content v-if="users" :title="$t('adminPanel.titleUsers')" :inputTitle="$t('adminPanel.inputUserTitle')"  type="users" :dataInvoices="users" :headers="headersUsers">
                  <template slot-scope="{ data }">
                      <td class="table__data paddingSmall ">
                        <nuxt-link class="table__link" :to="`/adminPanel/${data._id}`"> <p>{{ data.username }}</p></nuxt-link>
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
                      {{ Math.round(data.balance_usdt + data.usdt_in_invoices) }}
                      </td>
                      <td class="table__data paddingNull" style="text-align:center;">
                        {{ data.contract_balance }}
                      </td>
                      <td class="table__data paddingNull" style="text-align:center;">
                          {{data.ethereum_balance ? data.ethereum_balance / (10**18) : null}}
                      </td>
                      <td class="table__data paddingSmall" style="text-align:center; padding-right:10px;">
                            <Select
                              :v-model="data.is_active ? 'Активный': 'Неактивный'"
                              :width="130"
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
                <!-- tab Deal -->
                <Content :key="componentInvoice" v-if="invoiceBoolean" :title="$t('adminPanel.deal')" :inputTitle="$t('adminPanel.inputDealTitle')" type="deal" :dataInvoices="dataInvoice" :headers="headersInvoice">
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
                        <td class="table__data paddingNull" style="text-align:center;">
                            <Button :disabled="disabledBtnFreeze(data.status)" :class="disabledBtnFreeze(data.status) ? null : 'green'" @click.native="freeze(data)" style="border-radius:50%; padding:0; height:40px;width:40px; margin-top:10px;" rounded outlined green></Button>
                        </td>
                        <td class="table__data paddingNull" style="text-align:center;">
                            <Button :disabled="disabledBtnCancel(data.status)" :class="disabledBtnCancel(data.status) ? null : 'green'" @click.native="cancel(data)" style="border-radius:50%; padding:0; height:40px;width:40px; margin-top:10px;" rounded outlined green></Button>
                        </td>
                        <td class="table__data paddingNull" style="text-align:center;">
                            <Button :disabled="disabledBtnConfirm(data.status)" :class="disabledBtnConfirm(data.status) ? null : 'green'" @click.native="confirm(data)" style="border-radius:50%; padding:0; height:40px;width:40px; margin-top:10px; " rounded outlined green></Button>
                        </td>
                    </template>
                </Content>
            </tab>
      </Tabs>
  </div>
</template>

<script>
import Tabs from '@/components/tabsAdminPanel/Tabs'
import Tab from '@/components/tabsAdminPanel/Tab'
import Content from '@/components/AdminPanel/Content'
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
                this.$t('adminPanel.headerInvoices.dateTime'),
                this.$t('adminPanel.headerInvoices.partiesOfTheTransaction'),
                this.$t('adminPanel.headerInvoices.amount'),
                this.$t('adminPanel.headerInvoices.status'),
                this.$t('adminPanel.headerInvoices.freeze'),
                this.$t('adminPanel.headerInvoices.reset'),
                this.$t('adminPanel.headerInvoices.sendForcibly'),
            ],
            headersUsers: [
                this.$t('adminPanel.headersUsers.name'),
                this.$t('adminPanel.headersUsers.mail'),
                this.$t('adminPanel.headersUsers.walletAddress'),
                this.$t('adminPanel.headersUsers.balanceUSDT'),
                this.$t('adminPanel.headersUsers.balanceUserWallet'),
                this.$t('adminPanel.headersUsers.balanceETH'),
                this.$t('adminPanel.headersUsers.status'),
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
        disabledBtnCancel(status){
            switch(status){
                case 'frozen':
                    return false
                    break
                case 'waiting_for_tokens':
                    return false
                    break
                case 'waiting_for_payment':
                    return false
                    break
                default:
                    return true
                break
            }
        },
        disabledBtnFreeze(status){
            switch(status){
                case 'frozen':
                    return true
                    break
                case 'waiting_for_tokens':
                    return false
                    break
                case 'waiting_for_payment':
                    return false
                    break
                default:
                    return true
                break
            }
        },
        disabledBtnConfirm(status){
            switch(status){
                case 'waiting_for_tokens':
                    return false
                    break
                case 'waiting_for_payment':
                    return false
                    break
                case 'frozen':
                    return false
                break
                default:
                    return true
                break
            }
        },
        async freeze(data){
            let res = await this.$axios.put(`/admin/invoice/${data._id}/freeze/`);
            if(res.status == 200){
                this.$store.dispatch('adminPanel/editStatus', {id: data._id, status:'frozen'})
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
        async cancel(data){
            try{
                let res = await this.$axios.put(`/admin/invoice/${data._id}/cancel/`)
                if(res){
                    this.$store.dispatch('adminPanel/editStatus', {id:data._id, status:'cancelled'})
                }
            }catch(e){
                console.log(e);
            }
        },
        async confirm(data){
            let res = await this.$axios.put(`/admin/invoice/${data._id}/transfer/`)
            .then((e)=>{
                this.$store.dispatch('adminPanel/editStatus', {id:data._id, status:'completed'})
            })
        },
        bannedOrActive(active,banned){
            let res;

            if(active && banned){
               return  res =  2
            }
            if(!active){
                return  res = 3
            }

            if(active && !banned){
                return 1
            }
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
    .green{
        background-color: #48B190 !important;
    }
    .table__link{
      text-decoration: underline;
      color:#48B190;
      position: relative;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
    }
</style>
