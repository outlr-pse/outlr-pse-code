import {createStore} from "vuex";
import auth from "./modules/auth";
import createPersistedState from "vuex-persistedstate";

export default createStore({
    modules: {
        auth
    },
    plugins: [createPersistedState()]
})