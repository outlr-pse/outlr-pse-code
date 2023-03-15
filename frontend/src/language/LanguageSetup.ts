import { Languages } from './Languages'
import en from './translations/en.json'
import de from './translations/de.json'
import { createI18n } from 'vue-i18n'

/**
 * This file contains the setup for the i18n library.
 */
const translations = {
  en,
  de
}
/**
 * This is the i18n instance that is used in the application.
 */
export const i18n = createI18n({
  locale: Languages.ENGLISH,
  fallbackLocale: Languages.ENGLISH,
  messages: translations
})
