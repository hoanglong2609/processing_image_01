<template lang="pug">
  div
    header-bar
    processing-image-base(
      ref="processing_image_base"
      mode="Grading"
    )
</template>

<script>
import {defineComponent} from "vue";
import {ProcessingImageBase, HeaderBar} from '@/components'

const Grading = defineComponent({
  components: {ProcessingImageBase, HeaderBar},
  setup() {
    return {}
  }
})

export default Grading
</script>