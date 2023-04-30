<template lang="pug">
  dialog-container(
    :label="label"
    :mode="isAdd ? 'create' : 'update'"
    :loading="loading"
    @on-close="$emit('on-close')"
    @on-update="updateItem"
    @on-create="createItem"
    v-model="show"
    :width="400"
  )
    v-text-field(
      ref="name"
      label="name"
      v-model="masterData.name"
    )
    v-text-field(
      ref="password"
      label="password"
      type="password"
      v-model="masterData.password"
    )
</template>


<script>
import {defineComponent, ref, watch, toRefs} from "vue";
import DialogContainer from "@/components/DialogContainer/index.vue";
import {createData, updateData} from "@/utils";

const Subject = defineComponent({
  components: {DialogContainer},
  props: {
    show: {
      type: Boolean,
      required: true
    },
    itemData: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: ''
    },
    isAdd: {
      default: true
    }
  },
  setup(props, {emit}) {
    const {itemData} = toRefs(props)
    const masterData = ref({})

    const convertData = () => {
      Object.keys(masterData.value).forEach((key) => {
        if (masterData.value[key] === '') masterData.value[key] = null
      })
    }

    const updateItem = async () => {
      convertData()
      await updateData('/subject/', masterData.value.id, masterData.value)
      emit('reload')
    }

    const createItem = async () => {
      await createData('/subject/', masterData.value)
      emit('reload')
    }

    const init = async () => {
      masterData.value = props.isAdd ? {name: '', password: ''} : {...itemData.value}
    }

    watch(
      () => props.show,
      () => {
        if (props.show) init()
      }
    )

    return {
      createItem,
      updateItem,
      masterData
    }
  }
})

export default Subject
</script>