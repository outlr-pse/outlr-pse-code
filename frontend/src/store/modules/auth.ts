import { type AuthModuleState } from './auth.state'
import { type ActionContext } from 'vuex'
import { requestTokenIdentity } from '../../api/APIRequests'

const defaultUsername = 'Not logged in'
const hasValidAuthToken: boolean = false
const username: string = defaultUsername

export default {
  namespaced: true,
  state: {
    isAuthenticated: hasValidAuthToken,
    username
  },
  actions: {
    async setAuthenticated (context: ActionContext<AuthModuleState, any>) {
      const userJson = await requestTokenIdentity()
      if ('username' in userJson) {
        context.commit('setAuthenticated')
        context.commit('setUsername', userJson.username)
      }
    },
    unsetAuthenticated (context: ActionContext<AuthModuleState, any>) {
      context.commit('unsetAuthenticated')
      context.commit('unsetUsername')
    }
  },
  mutations: {
    setAuthenticated (state: AuthModuleState) {
      state.isAuthenticated = true
    },
    unsetAuthenticated (state: AuthModuleState) {
      state.isAuthenticated = false
    },
    setUsername (state: AuthModuleState, username: string) {
      state.username = username
    },
    unsetUsername (state: AuthModuleState) {
      state.username = defaultUsername
    }
  },
  getters: {
    isAuthenticated (state: AuthModuleState) {
      return state.isAuthenticated
    },
    username (state: AuthModuleState) {
      return state.username
    }
  }

}
