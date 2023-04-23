<template lang="pug">
  div
    header-bar
    h2.text-center.clr-red.pt-2 User
    j-master-menu-component(
      :search-info="searchInfo"
      :download-score="true"
      @inputting="handleSearchInput"
      @open-add-dialog="curUser = null, isOpenDialog = true"
    )
    j-master-item-list.pa-2(
      :headers="headers"
      :items="students.filter(s => s.role === 0)"
      :actions="actions"
      @click-icon="curUser = $event"
      @on-update="isOpenDialog = true"
      @go-to-master-detail="goToScore"
      @on-delete="onDelete"
    )

    j-master-item-list.pa-2(
      :headers="headers"
      :items="students.filter(s => s.role === 1)"
      :actions="actions"
      @click-icon="curUser = $event"
      @on-update="isOpenDialog = true"
      @on-delete="onDelete"
    )

      //@on-delete="openConfirmDelete"
      //@on-update="onClickOpenUpdateDialog"
    user-dialog(
      ref="user_dialog"
      :show="isOpenDialog"
      :item-data="curUser"
      :label="curUser ? 'Add' : 'Edit'"
      :is-add="curUser === null"
      @on-close="isOpenDialog = false"
      @reload="init"
    )
</template>

<script>
import {defineComponent, onMounted, ref, getCurrentInstance} from "vue";
import {JMasterItemList, UserDialog, JMasterMenuComponent, HeaderBar} from '@/components'
import {getData, urlPath, actions, deleteData} from "@/utils";
import {debounce} from "lodash";

const Student = defineComponent({
  components: {JMasterItemList, UserDialog, JMasterMenuComponent, HeaderBar},
  setup() {
    const instance = getCurrentInstance().proxy
    const {$router, $route} = instance
    const isOpenDialog = ref(false)
    const curUser = ref(null)
    const searchInfo = ref('')
    const headers = [
      {
        text: '',
        align: 'start',
        sortable: false,
        width: 5,
      },
      {
        text: 'name',
        sortable: false,
        value: 'name'
      },
      {
        text: 'role',
        sortable: false,
        value: 'role'
      },
      {
        text: '',
        align: 'right',
        sortable: false,
        value: 'action',
      }
    ]
    const students = ref([])
    const init = async () => {
      const {subject} = $route.query
      const data = await getData('/user/', {
        user: {subject: subject, search_info: searchInfo.value}
      })
      students.value = data.users
      instance.$forceUpdate()
    }

    const onDelete = async () => {
      await deleteData('/user/', curUser.value.id)
      await init()
    }

    const handleSearchInput = debounce((value) => {
      searchInfo.value = value
      init()
    }, 300)

    const goToScore = (student) => {
      $router.push({
        name: urlPath.Score.name,
        query: {
          ...$route.query,
          student: student.id
        }
      })
    }

    onMounted(async () => {
      await init()
    })

    return {
      headers,
      actions,
      students,
      goToScore,
      searchInfo,
      handleSearchInput,
      isOpenDialog,
      curUser,
      init,
      onDelete
    }
  }
})

export default Student
</script>

<style scoped lang="sass">
.clr-red
  color: red
</style>