<template>
<div class="adminPanel__wrapper" v-if="filterData">
    <div class="adminPanel__seachPanel">
        <h1 class="adminPanel__title">{{title}}</h1>
        <hr class="adminPanel__title"/>
        <!-- <input type="text"> -->
        <div class="adminPanel__wrapper_searchForm">
            <Input
            type="test"
            :header="inputTitle"
            style="margin-right:30px;"
            :width="500"
            v-model="input"
            />
            <Button @click.native="search" green>{{ $t('main.search') }}</Button>
        </div>
        <AppTable :propsContPage="6"  maxWidth="900px" :data="filterData" :headers="[...headers]" pagination>
            <template slot-scope="{ row }">
                <slot :data="row"></slot>
            </template>
        </AppTable>
    </div>
</div>
</template>

<script>
import Button from '@/components/app/Button'
import Input from '@/components/app/Input'
import AppTable from '@/components/app/AppTable'

export default {
    props:['title', 'dataInvoices', 'headers', 'type', 'inputTitle'],
    name:'Content',
    data(){
        return{
        input:'',
        filterData:null,
        }
    },
    components:{
        Button,
        Input,
        AppTable
    },
    methods:{
    async search(){
      let data;
      if(this.type == 'users'){
        data =  this.filterInvoice(this.dataInvoices, ['email', 'username'])
        if(data.length > 0) this.filterData = data
        if(data.length < 1){
          let {data} = await this.$axios.get(`/admin/users/?eth_address=${this.input}`);
          if(data.length > 0) this.filterData = data
        }
        this.$emit('clickPageOne', 1)
        return
      }
      if(this.type == 'deal'){
        data = this.filterInvoice(this.dataInvoices, ['buyer_username', 'seller_username', '_id'])
        this.filterData = data
        this.$emit('clickPageOne', 1)
        return
      }
    },
    filterInvoice(invoice, mass){
      // метод для поиска пользователей и сделок в админке.
      let result = []
      let flag = false
      invoice.forEach(e=> {
        mass.forEach(m=>{
          if
          (
            e[m]?.toLowerCase().indexOf(this.input.toLowerCase()) !== -1 &&
            e[m]?.toLowerCase().indexOf(this.input.toLowerCase()) !== undefined &&
            !flag
          )
          {
            result.push(e)
            flag = true
          }
        })
        flag = false
      })
      console.log(result);
      return result
    },
    },
    mounted(){
        this.filterData = this.dataInvoices
    }
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
</style>
