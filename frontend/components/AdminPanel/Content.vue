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
        let data = this.dataInvoices.filter(e=> {
            if(this.type === 'users'){
                    return  e.email?.indexOf(this.input) > -1 ||
                            e.username?.indexOf(this.input) > -1
            }
            if(this.type === 'deal'){
                if(e.buyer_nickname !== null){
                    return  e.buyer_nickname.indexOf(this.input) !== -1 ||
                            e.seller_nickname.indexOf(this.input) !== -1 ||
                            e._id.indexOf(this.input) !== -1
                }
            }
        })
        if(data.length > 0) this.filterData = data
        if(data.length < 1){
          let result = await this.$axios.get(`/admin/users/?eth_address=${this.input}`);
          if(result.data.length > 0) this.filterData = result.data
        }
        this.$emit('clickPageOne', 1)
    }
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
