<template lang="pug">
  dialog-container(
    label="Kết quả"
    @on-close="$emit('on-close')"
    v-model="show"
    :width="400"
  )
    template(v-slot:actions)
      span
    v-img(width="100%" height="100%" :src="url")

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
    url: {
      default: ''
    }
  },
  components: {DialogContainer},
  setup(props) {
    return {}
  }
})
</script>