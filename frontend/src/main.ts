import { LanguageService } from './language/LanguageService'
import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

const languageService = new LanguageService()

const i18n = createI18n({
  locale: languageService.getCurrentLocale(),
  fallbackLocale: 'en',
   messages: languageService.getTranslations()
 })

const app = createApp(App)

app.use(i18n)
app.mount('#app')
