<template lang="pug">
  div
    processing-image-base(
      ref="processing_image_base"
      mode="Grading"
    )
</template>

<script>
import {defineComponent} from "vue";
import {ProcessingImageBase} from '@/components'

const Grading = defineComponent({
  components: {ProcessingImageBase},
  setup() {
    return {}
  }
})

export default Grading
</script>