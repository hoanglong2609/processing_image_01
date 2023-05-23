<template lang="pug">
  dialog-container(
    label="Change password"
    @on-close="$emit('on-close')"
    v-model="show"
    :width="400"
  )
    v-text-field(
      ref="old_password"
      type="password"
      label="old_password"
      v-model="masterData.old_password"
    )
    v-text-field(
      ref="new_password"
      label="new_password"
      type="password"
      v-model="masterData.new_password"
    )
    v-text-field(
      ref="new_password"
      label="new_password"
      type="password"
      v-model="masterData.re_new_password"
    )
    template(v-slot:actions)
      .pa-4
        v-btn.relative-btn(
          dark
          block
          color="#f57e2e"
          @click="onSave"
        )
          | Save
</template>

<script>
import {defineComponent, getCurrentInstance} from "vue";
import DialogContainer from "@/components/DialogContainer/index.vue";
import {createData} from "@/utils";

const ChangePasswordDialog = defineComponent({
  components: {DialogContainer},
  props: ['show'],
  setup() {
    const instance = getCurrentInstance().proxy
    const {$toast} = instance
    const masterData = {
      id: JSON.parse(localStorage.getItem('user')).id,
      old_password: null,
      new_password: null,
      re_new_password: null
    }

    const onSave = async () => {
      if (masterData.new_password !== masterData.re_new_password) {
        $toast.error('Nhập lại mật khẩu')
        return
      }
      await createData('/user/change_password', masterData)
    }

    return {
      masterData,
      onSave
    }
  }
})

export default ChangePasswordDialog
</script>