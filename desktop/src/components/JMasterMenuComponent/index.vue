<template lang="pug">
  div.mt-0.mx-2.search
    v-text-field.mb-1.input(
      label="Search"
      outlined
      dense
      v-model="searchInfoValue"
      prepend-inner-icon="mdi-magnify"
      @input="onInput()"
      color="#f57e2e"
    )

    div.pl-10
      v-btn.mr-2.button(v-if="downloadScore" color="primary" dark @click="onDownload")
        v-icon mdi-cloud-download-outline
        span Download Score
      v-btn.mr-2.button(v-if="user.role === 1" color="primary" dark @click="$emit('open-add-dialog')")
        v-icon mdi-plus
        span Add

</template>

<script>
import {defineComponent, getCurrentInstance, ref, watch} from 'vue'
import {api} from "@/plugins";

export default defineComponent({
  props: {
    searchInfo: {
      type: String,
      required: true
    },
    downloadScore: {
      default: false
    }
  },
  setup(props, {emit}) {
    const instance = getCurrentInstance()
    const {$route, $toast} = instance.proxy
    const searchInfoValue = ref(props.searchInfo || '')
    const user = JSON.parse(localStorage.getItem('user'))

    const onDownload = async () => {
      const {subject} = $route.query
      try {
        const {data} = await api.get(`/score/csv?subject=${subject}`)

        const blob = new Blob([data], { type: 'application/csv' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.click()
        URL.revokeObjectURL(link.href)
      } catch (e) {
        $toast.error('Download failed')
      }
    }
    const onInput = () => {
      emit('inputting', searchInfoValue.value)
    }

    watch(
      () => props.searchInfo,
      () => {
        searchInfoValue.value = props.searchInfo
      }
    )

    return {
      onInput,
      searchInfoValue,
      onDownload,
      user
    }
  }
})
</script>

<style lang="sass">
.button
  height: 40px !important

.search
  max-width: 900px
  padding: 10px
  display: flex

  .divider
    background-color: var(--v-primary-base)

  .input
    .v-input__slot
      background: #ffffff
      min-height: 40px !important

    .v-input__slot:hover
      background: #ffffff !important

  .categories-list
    position: absolute
    left: 8px
    right: 8px
    z-index: 4
    overflow: auto
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.5)

    .category-title
      padding: 4px

      .v-icon
        color: var(--v-primary-base)
        padding: 2px !important

.v-application .mx-2
  margin: 0 auto !important

.green-bg-btn
  background-color: var(--v-primary-base)
  border-color: var(--v-primary-base)
</style>