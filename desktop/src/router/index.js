import Vue from 'vue'
import VueRouter from 'vue-router'
import store from "@/store";
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../pages/Home/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('user')
      if (token && from.name !== to.name) {
        store.commit('setTitle', 'Trang Chủ')
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
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
        store.commit('setTitle', 'Phòng Thi')
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
        store.commit('setTitle', 'Danh Sách Thành Viên')
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
        store.commit('setTitle', 'Điểm')
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
        store.commit('setTitle', 'Tạo Đáp Án')
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    path: '/manual_create_result',
    name: 'ManualCreateResult',
    component: () => import(/* webpackChunkName: "about" */ '../pages/ManualCreateResult/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('user')
      if (token && from.name !== to.name) {
        store.commit('setTitle', 'Tạo Đáp Án Thủ Công')
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
        store.commit('setTitle', 'Chấm Điểm')
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    path: '/user',
    name: 'User',
    component: () => import(/* webpackChunkName: "about" */ '../pages/User/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('user')
      if (token && from.name !== to.name) {
        store.commit('setTitle', 'Danh Sách Người Dùng')
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
        store.commit('setTitle', 'Đăng Nhập')
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
