<template>
  <notifications group="app" :closeOnClick="false" position="bottom right" class="localusd-toast__wrapper" width="400px">
    <template slot="body" slot-scope="props">
      <n-link :to="'/invoice/' + props.item.data.invoice_id" :class="['localusd-toast', props.item.type]">
        <div class="localusd-toast__header">
          <div class="localusd-toast__title-wrapper">
            <span>{{ $t('other.order') }} — </span>
            <div class="title" v-if="props.item.title">
              {{props.item.title}}
            </div>
            <div v-else class="title title--blue">
              {{ $t('other.new') }} 
            </div>
          </div>
          <span class="close" @click.prevent.stop="props.close">
            {{ $t('other.close') }}
          </span>
        </div>
        <div v-html="props.item.text">
        </div>
      </n-link>
    </template>
  </notifications>
</template>

<script>
export default {
  methods: {
  }
}
</script>

<style lang="scss">
.localusd-toast {
  display: block;
  padding: 15px 20px;
  margin-bottom: 15px;

  font-size: 15px;

  background: #F8F8F8;
  border: 1px solid #C8C8C8;
  color: #000000;
  min-height: 100px;
  border-radius: 5px;
  box-shadow: 0 5px 14px rgba(35, 50, 45, 0.2);

  .time {
    font-size: 13px;
    margin-top: 6px;
    color: #7f828b;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .close {
    cursor: pointer;
    font-size: 13px;
    color: #7f828b;
    padding: 10px;
    border-radius: 6px;
    &:hover {
      background-color: #e9e9e9;
      color: #ec5757;
    }
  }

  .title {
    font-size: 16px;
    font-weight: 600;
    color: #48B190;
    text-transform: capitalize;
    margin-bottom: 6px;
    display: inline-block;

    &--blue {
      color: #ED9F43;
    }
  }

  &.success {
    background: #48B190;
    //color: #48B190;
    border-left-color: #29886a;
    box-shadow: 0 5px 14px rgba(35, 50, 45, 0.3);
  }

  &__wrapper {
    margin-bottom: 30px;
    margin-right: 30px;

    .vue-notification-wrapper {
      overflow: visible !important;
    }
  }
}
</style>
