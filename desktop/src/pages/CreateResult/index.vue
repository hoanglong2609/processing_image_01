<template lang="pug">
  div
    processing-image-base(mode="CreateResult")
</template>

<script>
import {defineComponent} from "vue";
import {ProcessingImageBase} from '@/components'

const CreateResult = defineComponent({
  components: {ProcessingImageBase},
  setup() {
    return {}
  }
})

export default CreateResult
</script>