<template>
  <div class="profile-referral">
    <div class="profile-referral__header">
      <h2 class="profile-referral__title">Реферальная программа</h2>
      <p class="profile-referral__conditions" @click="showModal = true">Условия</p>
    </div>
    <div class="profile-referral__body">
      <Input
        value="https://localerc/1231213lsfd1221134dv"
        disabled
        header="Поделитесь этой ссылкой с друзьями"
        endIcon="copy"
      />
      <hr class="divider" />

      <div class="info">
        <div class="info__row">
          <p class="opacity-50 mb-15">Зарегистрировалось по ссылке:</p>
          <p class="opacity-50">Доход с реферальной программы:</p>
        </div>
        <div class="info__row">
          <p class="mb-15">12 человек</p>
          <p>800,00 USDT</p>
        </div>
      </div>
    </div>
    <ReferralModal :show="showModal" @toggleModal="toggleModal($event)" />
  </div>
</template>

<script>
import Input from '~/components/app/Input'
import ReferralModal from '~/components/ReferralModal'
export default {
  components: {
    Input,
    ReferralModal
  },
  data() {
    return {
      showModal: false
    }
  },
  methods: {
    toggleModal(state) {
      this.showModal = state
    }
  }
}
</script>

<style lang="scss">
.profile-referral {
  width: 400px;

  &__header {
    height: 20px;
    display: flex;
    align-items: center;
  }
  &__title {
    font-weight: 500;
  }

  &__conditions {
    margin-left: 10px;
    border: none;
    outline: none;
    background-color: white;
    font-size: 14px;
    padding: 0;
    color: $orange;
    cursor: pointer;
  }

  &__body {
    margin-top: 60px;

    .divider {
      margin-top: 20px;
      margin-bottom: 20px;
    }

    .info {
      display: flex;
      justify-content: space-between;
      // flex-direction: column;
      &__row {
        display: flex;
        justify-content: space-between;
        flex-direction: column;

        margin-top: 15px;
        // &:last-child {
        // }
      }
    }
  }
}
</style>
