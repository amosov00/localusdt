<template>
  <div v-if="locale === 'ru'" class="lang-switcher" @click="switchLang('en')">EN</div>
  <div v-else class="lang-switcher" @click="switchLang('ru')">RU</div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters({
      locale: 'i18n/GET_LOCALE',
      user: 'user',
      getLocaleIdByCode: 'i18n/GET_LOCALE_ID_BY_CODE'
    })
  },
  methods: {
    async switchLang(locale) {
      localStorage.setItem('locale', locale)

      if (this.user) {
        const localeId = this.getLocaleIdByCode(locale)
        await this.$store.dispatch('changeProfile', { language: localeId })

      }

      location.reload()
    }
  }
}
</script>

<style lang="scss">
.lang-switcher {
  color: $green;
  cursor: pointer;
}
</style>
