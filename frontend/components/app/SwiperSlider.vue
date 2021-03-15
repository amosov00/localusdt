<template>
    <swiper  class="swiper" :options="swiperOptions">
        <swiper-slide >
            <img class="imgSlider" src="https://i.ibb.co/kHfGXvx/Frame-2.png" alt="">
        </swiper-slide>
        <swiper-slide>
            <img class="imgSlider" src="https://i.ibb.co/kHfGXvx/Frame-2.png" alt="">
        </swiper-slide>
        <div class="swiper-pagination" slot="pagination"></div>
    </swiper>
</template>

<script>
import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
import 'swiper/css/swiper.css'
export default {
    data(){
        return{
            swiperOptions: {
                pagination: {
                    el: '.swiper-pagination',
                    type: 'bullets',
                    clickable:true,
                    bulletActiveClass:'pagination-active'
                },
                 autoplay: {
                    delay: 15000,
                },
            },
        }
    },
    components:{
        Swiper, SwiperSlide
    }
}
</script>

<style>
    .swiper{
        height: 216px;
    }
    .pagination-active{
        width: 30px;
        border-radius: 5px;
        transition:all 0.5s;
        background-color: #ED9F43 !important;
        opacity: 1;
    }
    .swiper-pagination-bullet{
        background-color: white ;
        opacity: 20 !important;
    }
    .imgSlider{
        width: 100%;
        height: inherit;
    }
</style>
