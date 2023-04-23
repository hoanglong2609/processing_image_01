import Vue from 'vue'
import VueRouter from 'vue-router'
import store from "@/store";
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Subject',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../pages/Subject/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('user')
      if (token && from.name !== to.name) {
        store.commit('setTitle', 'Subject')
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    path: '/student',
    name: 'Student',
    component: () => import(/* webpackChunkName: "about" */ '../pages/Student/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('user')
      if (token && from.name !== to.name) {
        store.commit('setTitle', 'User')
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    path: '/score',
    name: 'Score',
    component: () => import(/* webpackChunkName: "about" */ '../pages/Score/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('user')
      if (token && from.name !== to.name) {
        store.commit('setTitle', 'Score')
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    path: '/create_result',
    name: 'CreateResult',
    component: () => import(/* webpackChunkName: "about" */ '../pages/CreateResult/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('user')
      if (token && from.name !== to.name) {
        store.commit('setTitle', 'CreateResult')
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    path: '/grading',
    name: 'Grading',
    component: () => import(/* webpackChunkName: "about" */ '../pages/Grading/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('user')
      if (token && from.name !== to.name) {
        store.commit('setTitle', 'Grading')
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "about" */ '../pages/Login/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('user')
      if (!token) {
        store.commit('setTitle', 'Login')
        next()
        return
      }
      next({ name: 'Subject' })
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
