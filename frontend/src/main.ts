import { createApp } from 'vue'
import './assets/main.css'
import App from './App.vue'
import { i18n } from './language/LanguageSetup'
import store from './store/index'
import { initialValidityCheck } from './api/AuthServices'
import router from './router'

const app = createApp(App)

app.use(i18n)
app.use(store)
app.use(router)

// initial validity check handled in App.vue by assigning function to onBeforeMount hook
app.mount('#app')
