import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    title: null,
    showAppBar: window.location.pathname !== '/login'
  },
  getters: {
  },
  mutations: {
    setTitle (state, value) {
      state.title = value
    },
    setShowAppBar (state, value) {
      state.showAppBar = value
    }
  },
  actions: {
  },
  modules: {
  }
})
