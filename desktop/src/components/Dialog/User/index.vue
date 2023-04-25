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
      ref="code"
      label="code"
      v-model="masterData.code"
    )
    v-text-field(
      ref="name"
      label="name"
      v-model="masterData.name"
    )
    v-text-field(
      ref="name"
      label="mail"
      v-model="masterData.mail"
    )
    v-autocomplete(
      multiple
      label="subject"
      item-text="name"
      item-value="id"
      :items="subjects"
      v-model="masterData.subject_ids"
    )
    v-checkbox(
      label="is teacher"
      v-model="masterData.role"
    )
</template>


<script>
import {defineComponent, ref, watch, toRefs, onMounted} from "vue";
import DialogContainer from "@/components/DialogContainer/index.vue";
import {createData, updateData, getData} from "@/utils";

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
    const subjects = ref([])

    const convertData = () => {
      Object.keys(masterData.value).forEach((key) => {
        if (masterData.value[key] === '') masterData.value[key] = null
      })
      masterData.value.password = masterData.value.code
      masterData.value.role = masterData.value.role ? 1 : 0
    }
    const updateItem = async () => {
      convertData()
      await updateData('/user/', masterData.value.id, masterData.value)
      emit('reload')
    }

    const createItem = async () => {
      convertData()
      await createData('/user/', masterData.value)
      emit('reload')
    }

    const init = async () => {
      masterData.value = props.isAdd
        ? {name: '', password: '', code: '', mail: '', role: false, subject_ids: []}
        : {...itemData.value, subject_ids: itemData.value.subjects.map(sj => sj.id)}
    }

    const getSubjects = async () => {
      subjects.value = (await getData(['subject'])).subjects
    }

    watch(
      () => props.show,
      () => {
        if (props.show) init()
      }
    )

    onMounted(getSubjects)

    return {
      createItem,
      updateItem,
      masterData,
      subjects
    }
  }
})

export default Subject
</script>