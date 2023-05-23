<template lang="pug">
  dialog-container(
    label="Login subject"
    @on-close="$emit('on-close')"
    v-model="show"
    :width="400"
  )
    v-text-field(
      label="Password"
      v-model="password"
      type="password"
    )
    template(v-slot:actions)
      .pa-4
        v-btn.relative-btn(
          dark
          block
          color="#f57e2e"
          @click="onLogin"
        )
          | Login
</template>

<script>
import {defineComponent, ref, getCurrentInstance} from "vue";
import DialogContainer from '../DialogContainer'
import {createData} from "@/utils";

const LoginSubjectDialog = defineComponent({
  components: {DialogContainer},
  props: ['show', 'subject'],
  setup(props, {emit}) {
    const instance = getCurrentInstance().proxy
    const {$toast} = instance
    const password = ref('')
    const onLogin = async () => {
      const data = await createData(
        '/subject/login',
        {id: props.subject, password: password.value},
        false
      )
      if (data.code === 200) {
        $toast.success('Login successful')
        emit('login-successful')
      } else {
        $toast.error('Login failed')
      }
    }
    return {
      onLogin,
      password
    }
  }
})

export default LoginSubjectDialog
</script>