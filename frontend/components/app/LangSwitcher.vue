<template>
  <div v-if="locale === 'ru'" class="lang-switcher" @click="switchLang('en')">EN</div>
  <div v-else class="lang-switcher" @click="switchLang('ru')">RU</div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters({
      locale: 'i18n/GET_LOCALE'
    })
  },
  methods: {
    switchLang(locale) {
      localStorage.setItem('locale', locale)
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