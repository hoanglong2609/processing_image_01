<template lang="pug">
  v-app
    v-app-bar(app color='#f57e2e' dark='' v-if="$store.state.showAppBar")
      v-app-bar-nav-icon(@click="drawer = !drawer")
      v-btn(icon @click="back()")
        v-icon mdi-arrow-left-thin
      v-toolbar-title {{$store.state.title}}

    v-main
      router-view

    v-navigation-drawer(v-model='drawer' absolute='' temporary='')
      v-list-item
        v-list-item-content
          v-list-item-title {{user}}
      v-divider
      v-list(dense='')
        v-list-item(v-for='item in menus' :key='item.text' link='' @click="goto(item)")
          v-list-item-icon
            v-icon {{ item.icon }}
          v-list-item-content
            v-list-item-title {{ item.text }}

</template>

<script>
import {urlPath} from '@/utils'
export default {
  name: 'App',

  data: () => ({
    drawer: false,
    menus: [
      {icon: 'mdi-clipboard-list-outline', text: 'Danh Sách Lớp', page: urlPath.Subject},
      {icon: 'mdi-notebook-check-outline', text: 'Chấm Điểm', page: urlPath.Grading},
      {icon: 'mdi-notebook-plus-outline', text: 'Tạo Đáp Án', page: urlPath.CreateResult},
      {icon: 'mdi-logout', text: 'Logout', page: urlPath.Login}
    ],
    user: JSON.parse(localStorage.getItem('user'))?.name
  }),
  methods: {
    back() {
      this.$router.back()
    },
    goto(menu) {
      if (menu.text === 'Logout') localStorage.clear()
      this.$router.push({name: menu.page.name}).catch(() => {})
    }
  }
};
</script>
