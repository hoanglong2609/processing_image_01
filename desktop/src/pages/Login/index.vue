<template lang="pug">
  .pt-10
    v-card(class="mx-auto" max-width="344" )
      v-card-title.bg.white--text(color="#f57e2e" ) Đăng nhập
      v-card-text
        v-text-field(label="mssv" v-model="info.code")
        v-text-field(label="password" v-model="info.password" type="password" )
      v-card-actions
        v-row
          v-col(cols="6")
            v-btn.white--text(width="100%" color="red" @click="onForgotPass") Quên mật khẩu
          v-col(cols="6")
            v-btn.white--text(width="100%" color="#f57e2e" @click="onLogin") Đăng nhập

    forgot-pass(
      :show="showForgotPass"
      @on-close="showForgotPass = false"
    )
</template>

<script>
import {defineComponent, getCurrentInstance, onMounted, ref} from "vue";
import {createData, urlPath} from '@/utils'
import ForgotPass from "@/pages/Login/ForgotPass.vue";

const Login = defineComponent({
  components: {ForgotPass},
  setup() {
    const instance = getCurrentInstance().proxy
    const {$router, $store, $toast} = instance
    const info = {
      code: null,
      password: null
    }
    const showForgotPass = ref(false)

    const onLogin = async () => {
      const data = await createData('/user/login/', info, false)
      if (data.code === 200) {
        localStorage.setItem('user', JSON.stringify(data.data))
        await $router.push({name: urlPath.Subject.name})
        $store.commit("setShowAppBar", true)
      } else {
        $toast.error('Login failed')
      }
    }
    const onForgotPass = () => {
      showForgotPass.value = true
    }

    onMounted(() => {
      $store.commit("setShowAppBar", false)
    })

    return {
      info,
      onForgotPass,
      onLogin,
      showForgotPass
    }
  }
})
export default Login
</script>

<style lang="sass" scoped>
.bg
  background-color: #f57e2e
</style>