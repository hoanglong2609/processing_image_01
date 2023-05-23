<template lang="pug">
  div
    header-bar
    h2.text-center.clr-red.pt-2 Score
    j-master-item-list.pa-2(
      :headers="headers"
      :items="scores"
      :actions="actions"
    )
      //@on-delete="openConfirmDelete"
      //@on-update="onClickOpenUpdateDialog"
</template>

<script>
import {defineComponent, onMounted, ref, getCurrentInstance} from "vue";
import {JMasterItemList, HeaderBar} from '@/components'
import {getData, urlPath, actions} from "@/utils";

const Score = defineComponent({
  components: {JMasterItemList, HeaderBar},
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
        text: 'score',
        sortable: false,
        value: 'score'
      }
    ]

    const scores = ref([])
    const init = async () => {
      const {subject, student} = $route.query
      const data = await getData('/score/', {score: {subject: subject, student: student}})
      scores.value = data.scores
    }

    onMounted(async () => {
      await init()
    })

    return {
      headers,
      actions,
      scores
    }
  }
})

export default Score
</script>

<style scoped lang="sass">
.clr-red
  color: red
</style>