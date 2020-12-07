<template>
    <div>
        <div class="tabs">
            <ul class="list-type-none tabs__ul">
                <li v-for="(tab, i) in tabs" @click="selectTab(tab)" :class="{ 'active': tab.isActive }" class="tabs__li" :key="i">
                    <div  :class="{ 'circle__select active': tab.isActive }" class="circle__select">{{tab.name}}</div>
                </li>
            </ul>
            <div class="tabs-details">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name:'Tabs',
    data: ()=>({
        tabs:[]
    }),
    methods:{
        selectTab(selectedTab) {
            this.tabs.forEach(tab => {
                tab.isActive = (tab.name == selectedTab.name);
            });
        }

    },
    created(){
        this.tabs = this.$children
    }
}
</script>

<style lang="scss" scoped>

    .tabs{
        display: flex;
    }
    .tabs__ul{
        min-width: 20%;
        list-style-type: none;
        background-color: #FAFAFA;
        height: inherit;
        display: flex;
        flex-direction: column;
        align-content: center;
        text-align: right;
        padding-top: 150px;
        line-height: 50px;
    }
    .tabs__li{
        height: 50px;
        padding-right: 20px;
        cursor: pointer;
    }
    .active{
         background-color: #48B190;
         color:#FFFFFF;
    }
</style>