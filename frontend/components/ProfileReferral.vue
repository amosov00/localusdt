<template>
  <div class="profile-referral">
    <div class="profile-referral__header">
      <h2 class="profile-referral__title">{{ $t('profile.refProgram') }}</h2>
      <p class="profile-referral__conditions"
         @click="showModal = true">
        {{ $t('profile.terms') }}
      </p>
    </div>
    <div class="profile-referral__body">
      <Input
        :value="referralId"
        disabled
        :header="$t('profile.link')"
        endIcon="copy"
      />
      <Input
        class="profile-referral__code"
        :value="referralInfo.referral_id"
        disabled
        :header="$t('profile.refCode')"
        endIcon="copy"
        :toastText="$t('profile.copied')"
      />
      <hr class="divider" />

      <div class="info">
        <div class="info__row">
          <p class="opacity-50 mb-15">{{$t('profile.signUpByLink')}}</p>
          <p class="opacity-50">{{$t('profile.earn')}}</p>
        </div>
        <div class="info__row">
          <p class="mb-15">{{referralInfo.referral_count}} {{$t('profile.people')}}</p>
          <p>{{spaceSplitting(referralInfo.income)}} USDT</p>
        </div>
      </div>
    </div>
    <ReferralModal :show="showModal" @toggleModal="toggleModal($event)" />
  </div>
</template>

<script>
import Input from '~/components/app/Input'
import ReferralModal from '~/components/ReferralModal'
import formatCurrency from '~/mixins/formatCurrency'

export default {
  mixins: [formatCurrency],
  components: {
    Input,
    ReferralModal
  },
  data() {
    return {
      showModal: false,
      referralInfo: {
        income: 0,
        referral_count: 0,
        referral_id: ''
      }
    }
  },
  async mounted() {
    let referralInfo = await this.$store.dispatch('fetchReferralInfo')
    if (referralInfo) {
      this.referralInfo = referralInfo
    }

  },
  computed: {
    referralId() {
      return window.location.origin + '/ref?id=' + this.referralInfo.referral_id
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

  &__code {
    margin-top: 40px;
  }

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
