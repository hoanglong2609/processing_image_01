<template lang="pug">
  dialog-container(
    label="Quên Mật Khẩu"
    @on-close="$emit('on-close')"
    v-model="show"
    :width="400"
  )
    v-text-field(
      label="code" v-model="body.code"
    )
    v-text-field(
      label="mail" v-model="body.gmail"
    )
    template(v-slot:actions)
      .pa-4
        v-btn.relative-btn(
          dark
          block
          color="#f57e2e"
          @click="onForgot"
        )
          | Lấy Mật Khẩu
</template>

<script>
import Vue, {defineComponent} from "vue";
import {DialogContainer} from '@/components'
import {api} from '@/plugins'

const ForgotPass = defineComponent({
  components: {DialogContainer},
  props: ['show'],
  setup (props, {emit}) {
    const body = {
      code: null, gmail: null
    }

    const onForgot = async () => {
      try {
        await api.get(`/user/forgot?code=${body.code}&gmail=${body.gmail}`)
        Vue.$toast.error('Please check mail')
        emit('on-close')
      } catch (e) {
        Vue.$toast.error('get data failed')
      }
    }

    return {
      body,
      onForgot
    }
  }
})

export default ForgotPass
</script>