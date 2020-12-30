<template>
  <section>
        <h1 class="rate_H">
           {{  $t('rates.rateH') }}
        </h1>
        <h2 class="rate_H2">{{  $t('rates.rateContentTop') }}</h2>
        <h2 class="rate_H2">{{  $t('rates.rateContentBot') }}</h2>
  </section>
</template>

<script>
export default {

}
</script>

<style   scoped>
.rate_H{
    padding-top: 40px;
    padding-bottom: 40px;
    text-align: center;
    border-bottom: 2px solid #f3f3f3;
}
.rate_H2{
    font-size: 25px;
    font-weight: 600;
    margin-bottom: 20px;
    margin-top: 40px;
}
.rate_p{
    margin-bottom: 20px;
}
ul > li {
  line-height: 30px;
  margin-bottom: 15px;
}
</style>
