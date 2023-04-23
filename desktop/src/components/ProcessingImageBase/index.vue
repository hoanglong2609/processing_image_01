<template lang="pug">
  div
    v-row.my-row
      v-col(cols="12" sm="4")
        v-autocomplete(
          outlined dense item-value="id" item-text="name" :items="subjects" @input="onLogin"
          v-model="bodyProcess.subject"
        )
      v-col(cols="12" sm="4")
        v-btn.white--text(width="100%" color="#f57e2e" @click="handleInput") Chọn Ảnh
      v-col(cols="12" sm="4")
        v-btn(width="100%" color="primary" :disabled="!isLogin" @click="onProcessing") Lưu
    v-divider
    input(
      multiple
      hidden
      ref="refInput"
      type="file"
      accept="image/*"
      @change="uploadImages"
    )
    v-row.my-row
      v-col(cols="6" v-for="img in listImage")
        v-img(:src="img.url" width="100%" )

    login-subject-dialog(
      :show="showLogin"
      :subject="bodyProcess.subject"
      @on-close="showLogin = false"
      @login-successful="showLogin = false, isLogin = true"
    )
    confirm-dialog(
      :showDialog="showConfirmDialog"
      :messages="confirmMsg"
      cancel-text="cancel"
      ok-text="yes"
      @on-cancel="showConfirmDialog=false"
      @on-close="showConfirmDialog=false"
      @on-ok="onConfirmOk"
    )
</template>

<script>
import {defineComponent, onMounted, ref, getCurrentInstance} from "vue";
import {getData, readFile, createData} from '@/utils'
import LoginSubjectDialog from "./loginSubjectDialog.vue";
import ConfirmDialog from "../Dialog/Confirm/index.vue";
import {api} from "@/plugins";

const ProcessingImageBase = defineComponent({
  components: {LoginSubjectDialog, ConfirmDialog},
  props: ['mode'],
  setup(props) {
    const instance = getCurrentInstance().proxy
    const {$refs, $toast} = instance
    const listImage = ref([])
    const isLogin = ref(false)
    const subjects = ref([])
    const showLogin = ref(false)
    const showConfirmDialog = ref(false)
    const confirmMsg = ref([])

    const bodyProcess = {
      subject: null,
      image: [],
      is_result: props.mode === 'CreateResult',
      is_overwrite: false,
      grading_again: false
    }

    const onProcessing = async () => {
      bodyProcess.image = listImage.value.map(img => img.payload)
      api.post('/processing_image/base64_img', bodyProcess)
        .then((response) => {
          $toast.success('create successful')
        })
        .catch((error) => {
          if (error.response.data.detail === 'result already exists') {
            confirmMsg.value = ['Duplicate', 'Would you like overwrite?']
            showConfirmDialog.value = true
          }
          $toast.error('create failed')
        })
    }

    const onConfirmOk = async () => {
      bodyProcess.is_overwrite = true
      if (confirmMsg.value.includes('Duplicate')) confirmMsg.value = ['Would you like to re-score?']
      else if (confirmMsg.value.includes('Would you like to re-score?') && bodyProcess.is_result) {
        bodyProcess.grading_again = true
        await onProcessing()
        showConfirmDialog.value = false
      } else {
        await onProcessing()
        showConfirmDialog.value = false
      }
      bodyProcess.grading_again = false
      bodyProcess.is_overwrite = false
      // await onProcessing()
    }

    const onLogin = () => {
      isLogin.value = false
      showLogin.value = true
      console.log('onLogin')
    }

    const init = async () => {
      const data = await getData(['subject'])
      subjects.value = data.subjects
    }

    const handleInput = () => {
      $refs.refInput.click()
    }

    const uploadImages = async () => {
      const files = $refs.refInput.files ? Object.values($refs.refInput.files) : []
      const body = await Promise.all(
        files.map(async (file) => {
          const payload = await readFile(file)
          return {
            payload,
            id: null,
            name: file.filename,
            type: file.type,
            size: file.filesize,
            url: URL.createObjectURL(file)
          }
        })
      )
      // listImage.value = [...listImage.value, ...body]
      listImage.value = [...body]
    }

    onMounted(init)

    return {
      subjects,
      uploadImages,
      handleInput,
      listImage,
      onLogin,
      showLogin,
      bodyProcess,
      isLogin,
      onProcessing,
      showConfirmDialog,
      onConfirmOk,
      confirmMsg
    }
  }
})

export default ProcessingImageBase
</script>

<style scoped lang="sass">
.my-row
  max-width: 1000px
  margin: 0 auto
</style>