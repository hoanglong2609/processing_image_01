<template lang="pug">
  div
    header-bar
    h2.text-center.clr-red.pt-2 Điểm
    j-master-item-list.pa-2(
      :headers="headers"
      :items="scores"
      :actions="actions"
    )
      template(v-slot:item.student="{item}")
        span {{item.student.name}}
      template(v-slot:item.answer="{item}")
        a(@click="openImageDialog = true, urlImage=item.image.url") bài làm
      template(v-slot:item.result="{item}")
        a(@click="onOpenResultDialog(item)") Kết quả
      //@on-delete="openConfirmDelete"
      //@on-update="onClickOpenUpdateDialog"

    result-dialog(
      :show="openResultDialog"
      :result="resultData"
      :filled-cell="filledCellData"
      @on-close="openResultDialog = false"
    )

    image-dialog(
      :show="openImageDialog"
      :url="urlImage"
      @on-close="openImageDialog = false"
    )
</template>

<script>
import {defineComponent, onMounted, ref, getCurrentInstance} from "vue";
import {JMasterItemList, HeaderBar} from '@/components'
import {getData, urlPath, actions} from "@/utils";
import {ResultDialog, ImageDialog} from "@/components";

const Score = defineComponent({
  components: {JMasterItemList, HeaderBar, ResultDialog, ImageDialog},
  setup() {
    const instance = getCurrentInstance().proxy
    const {$router, $route} = instance

    const headers = [
      {
        text: '',
        align: 'start',
        sortable: false,
        width: 5,
      },
      {
        text: 'code',
        sortable: false,
        value: 'code'
      },
      {
        text: 'student',
        sortable: false,
        value: 'student'
      },
      {
        text: 'score',
        sortable: false,
        value: 'score'
      },
      {
        text: 'answer',
        sortable: false,
        value: 'answer'
      },
      {
        text: 'result',
        sortable: false,
        value: 'result'
      }
    ]

    const openResultDialog = ref(false)

    const scores = ref([])
    const resultData = ref([])
    const filledCellData = ref([])
    const openImageDialog = ref(false)
    const urlImage = ref('')

    const init = async () => {
      const {subject, student} = $route.query
      const data = await getData('/score/', {score: {subject: subject, student: student}})
      scores.value = data.scores
    }

    const onOpenResultDialog = (item) => {
      openResultDialog.value = true
      resultData.value = item.result
      filledCellData.value = item.filled_cell
    }

    onMounted(async () => {
      await init()
    })

    return {
      headers,
      actions,
      scores,
      openResultDialog,
      onOpenResultDialog,
      resultData,
      openImageDialog,
      urlImage,
      filledCellData
    }
  }
})

export default Score
</script>

<style scoped lang="sass">
.clr-red
  color: red
</style>