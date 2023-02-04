import { createApp } from 'vue'
import './assets/main.css'
import App from './App.vue'
import {i18n} from "./language/LanguageSetup";
import store from "./store";
import {getIdentity} from "./api/DataRetrievalService";

const app = createApp(App)

app.use(i18n)
app.use(store)
app.mount('#app')

let identityJson = await getIdentity()

if ("username" in identityJson) {
    await store.dispatch("auth/setAuthenticated")
}

