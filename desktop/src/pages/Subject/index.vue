<template lang="pug">
  div
    header-bar
    h2.text-center.clr-red.pt-2 Subjects
    j-master-menu-component(
      :search-info="searchInfo"
      @inputting="handleSearchInput"
      @open-add-dialog="curSubject = null, isOpenDialog = true"
    )
    j-master-item-list.pa-2(
      :headers="headers"
      :items="subjects"
      :actions="actions"
      @click-icon="curSubject = $event"
      @go-to-master-detail="goToStudent"
      @on-update="isOpenDialog = true"
      @on-delete="onDelete"
    )
      //@on-delete="openConfirmDelete"
      //@on-update="onClickOpenUpdateDialog"
    subject-dialog(
      ref="subject_dialog"
      :show="isOpenDialog"
      :item-data="curSubject"
      :label="curSubject ? 'Add' : 'Edit'"
      :is-add="curSubject === null"
      @on-close="isOpenDialog = false"
      @reload="init"
    )
</template>

<script>
import {defineComponent, onMounted, ref, getCurrentInstance} from "vue";
import {JMasterItemList, SubjectDialog, JMasterMenuComponent, HeaderBar} from '@/components'
import {getData, urlPath, headers, actions, deleteData} from "@/utils";
import {debounce} from 'lodash'

const Subject = defineComponent({
  components: {JMasterItemList, SubjectDialog, JMasterMenuComponent, HeaderBar},
  setup() {
    const instance = getCurrentInstance().proxy
    const {$router} = instance
    const subjects = ref([])
    const isOpenDialog = ref(false)
    const curSubject = ref(null)
    const searchInfo = ref('')

    const init = async () => {
      const data = await getData('/subject/', {subject: {search_info: searchInfo.value}})
      subjects.value = data.subjects
      instance.$forceUpdate()
    }

    const handleSearchInput = debounce((value) => {
      searchInfo.value = value
      init()
    }, 300)

    const onDelete = async () => {
      await deleteData('/user/', curUser.value.id)
      await init()
    }

    const goToStudent = (subject) => {
      $router.push({
        name: urlPath.Student.name,
        query: {
          subject: subject.id
        }
      })
    }

    onMounted(async () => {
      await init()
    })

    return {
      headers,
      actions,
      subjects,
      goToStudent,
      isOpenDialog,
      curSubject,
      init,
      searchInfo,
      handleSearchInput,
      onDelete
    }
  }
})

export default Subject
</script>

<style scoped lang="sass">
.clr-red
  color: red
</style>