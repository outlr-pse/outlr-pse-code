import {getIdentity} from "../../api/DataRetrievalService"
import {AuthModuleState} from "./auth.state";
import {ActionContext} from "vuex";

const defaultUsername = "Not logged in"
let hasValidAuthToken:boolean = false
let username:string = defaultUsername



export default {
    namespaced:true,
    state:{
        isAuthenticated : hasValidAuthToken,
        username : username
    },
    actions:{
        async setAuthenticated(context : ActionContext<AuthModuleState, any>) {
            let userJson = await getIdentity()
            if ("username" in userJson) {
                context.commit('setAuthenticated')
                context.commit('setUsername', userJson.username)
            }
        },
        unsetAuthenticated(context : ActionContext<AuthModuleState, any>) {
            context.commit('unsetAuthenticated')
            context.commit('unsetUsername')
        },
    },
    mutations:{
        setAuthenticated(state : AuthModuleState) {
            state.isAuthenticated = true
        },
        unsetAuthenticated(state : AuthModuleState) {
            state.isAuthenticated = false
        },
        setUsername(state:AuthModuleState, username:string) {
            state.username = username
        },
        unsetUsername(state:AuthModuleState) {
            state.username = defaultUsername
        }
    },
    getters:{
        isAuthenticated(state:AuthModuleState) {
            return state.isAuthenticated
        },
        username(state :AuthModuleState) {
            return state.username
        }
    }

}