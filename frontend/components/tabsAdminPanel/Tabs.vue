<template>
    <div>
        <div :class="{'tabs': vertical}">
            <ul class="list-type-none " :class="{'tabs__ul' : vertical, 'tabs__ul2' : !vertical } ">
                <li v-for="(tab, i) in tabs" @click="selectTab(tab)"
                    :class="{ 'active': tab.isActive, 'tabs__li' : vertical, 'tabs__li2': !vertical  }"
                    :key="i">
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
    props:{
      vertical: Boolean
    },
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
    .tabs__ul2{
      list-style-type: none;
      background-color:transparent;
      display: flex;
      justify-content: center;
      padding-top: 30px;
    }
    .tabs__li{
        height: 50px;
        padding-right: 20px;
        cursor: pointer;
    }
    .tabs__li2{
      line-height: 40px;
      min-width: 100px;
      text-align: center;
      padding: 0 20px;
      cursor: pointer;
    }
    .active{
         background-color: #48B190;
         color:#FFFFFF;
    }
</style>
