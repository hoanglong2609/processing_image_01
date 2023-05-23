<template lang="pug">
  div
    v-app-bar(app color='#f57e2e' dark='' v-if="$store.state.showAppBar")
      v-app-bar-nav-icon(@click="drawer = !drawer")
      v-btn(icon @click="back()")
        v-icon mdi-arrow-left-thin
      v-toolbar-title {{$store.state.title}}

    v-navigation-drawer(v-model='drawer' absolute='' temporary='')
      v-list-item
        v-list-item-content
          v-list-item-title {{user?.name || ''}}
      v-divider
      v-list(dense='')
        v-list-item(v-for='item in menus' :key='item.text' link='' @click="goto(item)")
          v-list-item-icon
            v-icon {{ item.icon }}
          v-list-item-content
            v-list-item-title {{ item.text }}
    change-password-dialog(
      :show="openChangePasswordDialog"
      @on-close="openChangePasswordDialog = false"
    )
</template>

<script>
import {defineComponent, ref, getCurrentInstance} from "vue";
import {urlPath} from '@/utils'
import ChangePasswordDialog from '@/components/Dialog/ChangePassword/index.vue'
export default defineComponent({
  name: 'App',
  components: {ChangePasswordDialog},
  setup() {
    const instance = getCurrentInstance().proxy
    const {$router} = instance
    const user = localStorage.getItem('user') !== null ? JSON.parse(localStorage.getItem('user')) : null
    const drawer = ref(false)
    const openChangePasswordDialog = ref(false)
    const menus = JSON.parse(localStorage.getItem('user'))?.role !== 0
      ?
        [
          {icon: 'mdi-clipboard-list-outline', text: 'Danh Sách Phòng Thi', page: urlPath.Subject},
          {icon: 'mdi-clipboard-list-outline', text: 'Danh Sách Người Dùng', page: urlPath.User},
          {icon: 'mdi-notebook-check-outline', text: 'Chấm Điểm', page: urlPath.Grading},
          {icon: 'mdi-notebook-plus-outline', text: 'Tạo Đáp Án', page: urlPath.CreateResult},
          {icon: 'mdi-notebook-plus-outline', text: 'Tạo Đáp Án Thủ Công', page: urlPath.ManualCreateResult},
          {icon: 'mdi-key-outline', text: 'Đổi Mật Khẩu', page: null},
          {icon: 'mdi-logout', text: 'Logout', page: urlPath.Login}
        ]
      : [
          {icon: 'mdi-clipboard-list-outline', text: 'Danh Sách Lớp', page: urlPath.Subject},
          {icon: 'mdi-key-outline', text: 'Đổi Mật Khẩu', page: null},
          {icon: 'mdi-logout', text: 'Logout', page: urlPath.Login}
        ]

    const back = () => {
      $router.back()
    }
    const goto = (menu) => {
      if (menu.page === null) {
        openChangePasswordDialog.value = true
        return
      }
      if (menu.text === 'Logout') localStorage.clear()
      $router.push({name: menu.page.name}).catch(() => {})
      instance.$forceUpdate()
    }
    return {
      user,
      drawer,
      menus,
      openChangePasswordDialog,
      goto,
      back
    }
  }
})
</script>
