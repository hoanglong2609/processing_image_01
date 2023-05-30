<template lang="pug">
  dialog-container(
    label="Kết quả"
    @on-close="$emit('on-close')"
    v-model="show"
    :width="400"
  )
    template(v-slot:actions)
      span
    v-row
      v-col(cols="3" v-for="rs, index in resultShow")
        span {{rs.no}}: {{filledCellShow[index]?.value || ''}} / {{rs.value}}

</template>

<script>
import {defineComponent, computed} from "vue";
import DialogContainer from '@/components/DialogContainer/index.vue'

export default defineComponent({
  props: {
    show: {
      type: Boolean,
      required: true
    },
    result: {
      default: () => []
    },
    filledCell: {
      default: () => []
    }
  },
  components: {DialogContainer},
  setup(props) {
    const resultShow = computed(() => {
      const data = []
      props.result.forEach((key, index) => {
        let value = ''
        if (props.result[index] === 0) value = 'A'
        if (props.result[index] === 1) value = 'B'
        if (props.result[index] === 2) value = 'C'
        if (props.result[index] === 3) value = 'D'
        data.push({no: index + 1, value: value})
      })
      return data
    })

    const filledCellShow = computed(() => {
      const data = []
      props.filledCell.forEach((key, index) => {
        let value = ''
        if (props.filledCell[index] === 0) value = 'A'
        if (props.filledCell[index] === 1) value = 'B'
        if (props.filledCell[index] === 2) value = 'C'
        if (props.filledCell[index] === 3) value = 'D'
        data.push({no: index + 1, value: value})
      })
      return data
    })

    return {
      resultShow,
      filledCellShow
    }
  }
})
</script>