import { createApp } from 'vue'
import './assets/main.css'
import App from './App.vue'
import {i18n} from "./language/LanguageSetup";
import store from "./store/index";
import {initialValidityCheck} from "./api/AuthServices";

const app = createApp(App)

app.use(i18n)
app.use(store)

initialValidityCheck().then()

app.mount('#app')


