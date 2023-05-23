<template lang="pug">
  div
    header-bar
    v-row.my-row
      v-col(cols="12" sm="3")
        v-autocomplete(
          outlined dense item-value="id" item-text="name" :items="subjects" @input="onLogin"
          v-model="bodyProcess.subject"
        )
      v-col(cols="12" sm="3")
        v-text-field(
          label="Số câu" dense outlined v-model="numberOfQuestions" type="number"
        )
      v-col(cols="12" sm="3")
        v-text-field(
          label="Mã đề" dense outlined v-model="bodyProcess.code" type="number"
        )
      v-col(cols="12" sm="3")
        v-btn(width="100%" color="primary" :disabled="!isLogin" @click="onSave") Lưu
    v-divider
    v-row.my-row
      v-col(cols="6" sm="4" v-for="i in Number(numberOfQuestions)")
        multiple-choice.pa-3(:no="i" :value="result[i-1]" @on-choose="onChoose($event, i - 1)")
    login-subject-dialog(
      :show="showLogin"
      :subject="bodyProcess.subject"
      @on-close="showLogin = false"
      @login-successful="showLogin = false, isLogin = true"
    )
</template>

<script>
import {defineComponent, onMounted, ref, watch, getCurrentInstance} from "vue";
import {HeaderBar, MultipleChoice} from '@/components'
import {getData, createData} from "@/utils";
import LoginSubjectDialog from "@/components/ProcessingImageBase/loginSubjectDialog.vue";

const ManualCreateResult = defineComponent({
  components: {HeaderBar, LoginSubjectDialog, MultipleChoice},
  setup() {
    const instance = getCurrentInstance().proxy

    const subjects = ref([])
    const isLogin = ref(false)
    const showLogin = ref(false)
    const user = JSON.parse(localStorage.getItem('user'))
    const numberOfQuestions = ref(0)
    const result = ref([])

    const bodyProcess = {
      subject: null, code: null, result: []
    }

    const init = async () => {
      if (user.role === 3) {
        const data = await getData('/subject/')
        subjects.value = data.subjects
      } else {
        const data = await getData('/user/', {user: {id: user.id}})
        subjects.value = data.users[0].subjects
      }
    }

    const onChoose = (fillIndex, index) => {
      result.value[index] = fillIndex
      instance.$forceUpdate()
    }

    const onLogin = () => {
      isLogin.value = false
      showLogin.value = true
    }

    const onSave = async () => {
      bodyProcess.result = [...result.value]
      await createData('/result/', bodyProcess)
    }

    watch(
      () => numberOfQuestions.value,
      () => {
        result.value = result.value.slice(0, numberOfQuestions.value)
        for(let i = 0; i < numberOfQuestions.value; i++) {
          if (i >= result.value.length) result.value.push(0)
        }
      }
    )

    onMounted(init)

    return {
      subjects,
      isLogin,
      showLogin,
      onLogin,
      bodyProcess,
      numberOfQuestions,
      onChoose,
      result,
      onSave
    }
  }
})

export default ManualCreateResult
</script>

<style scoped lang="sass">
.my-row
  max-width: 1000px
  margin: 0 auto
</style>