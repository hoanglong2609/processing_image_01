<template lang="pug" xmlns="">
  div
    header-bar(ref="headerBar")
    v-row.my-row
      v-col(cols="6" v-for="menu in menus")
        .btn-menu(@click="goto(menu)")
          div
            v-icon(color="white" ) {{menu.icon}}
            span {{menu.text}}

</template>

<script>
import {defineComponent, getCurrentInstance} from "vue";
import {HeaderBar} from "@/components";
import {urlPath} from '@/utils'

const Home = defineComponent({
  components: {
    HeaderBar
  },
  setup() {
    const instance = getCurrentInstance().proxy
    const {$refs} = instance

    const menus = JSON.parse(localStorage.getItem('user'))?.role !== 0
      ?
        [
          {icon: 'mdi-clipboard-list-outline', text: 'Danh Sách Lớp', page: urlPath.Subject},
          {icon: 'mdi-clipboard-list-outline', text: 'Danh Sách Người Dùng', page: urlPath.User},
          {icon: 'mdi-notebook-check-outline', text: 'Chấm Điểm', page: urlPath.Grading},
          {icon: 'mdi-notebook-plus-outline', text: 'Tạo Đáp Án', page: urlPath.CreateResult},
          {icon: 'mdi-notebook-plus-outline', text: 'Tạo Đáp Án Thủ Công', page: urlPath.ManualCreateResult},
          {icon: 'mdi-key-outline', text: 'Đổi mật khẩu', page: null},
          {icon: 'mdi-logout', text: 'Logout', page: urlPath.Login}
        ]
      : [
          {icon: 'mdi-clipboard-list-outline', text: 'Danh Sách Lớp', page: urlPath.Subject},
          {icon: 'mdi-key-outline', text: 'Đổi mật khẩu', page: null},
          {icon: 'mdi-logout', text: 'Logout', page: urlPath.Login}
        ]

    const goto = (menu) => {
      $refs.headerBar.goto(menu)
    }

    return {
      menus,
      goto
    }
  }
})

export default Home
</script>

<style lang="sass" scoped>
.my-row
  max-width: 1000px
  margin: 0 auto
.btn-menu
  width: 100%
  color: white
  text-align: center
  background-color: #3535fc
  height: 60px
  border-radius: 10px
  cursor: pointer
.btn-menu div
  padding: 20px
</style>