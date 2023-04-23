<template lang="pug">
  div
    header-bar
    processing-image-base(mode="CreateResult")
</template>

<script>
import {defineComponent} from "vue";
import {ProcessingImageBase, HeaderBar} from '@/components'

const CreateResult = defineComponent({
  components: {ProcessingImageBase, HeaderBar},
  setup() {
    return {}
  }
})

export default CreateResult
</script>