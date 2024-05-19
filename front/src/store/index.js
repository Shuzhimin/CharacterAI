import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: null,
    navbarIndex: null,
  },
  mutations: {
    setToken(state, value){
      state.token = value
    },
    setNavbarIndex(state, value){
      state.navbarIndex = value
    }
  },
  getters:{
    getTokenValue: state => state.token,
    getNavbarIndex: state => state.navbarIndex
  },
  actions: {
  },
  modules: {
  }
})
