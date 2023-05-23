<template lang="pug">
  v-row
    v-col.pa-0(cols="2")
      span.no {{no}}
    v-col.pa-0(cols="10")
      v-row.pt-2
        v-col.pa-1(cols="3" @click="onChoose(0)")
          v-icon.ml-1(v-if="value === 0" color="green") mdi-check-circle
          v-icon.ml-1(v-if="value !== 0" color="#0000003d") mdi-checkbox-blank-circle-outline
          span A
        v-col.pa-1(cols="3" @click="onChoose(1)")
          v-icon.ml-1(v-if="value === 1" color="green") mdi-check-circle
          v-icon.ml-1(v-if="value !== 1" color="#0000003d") mdi-checkbox-blank-circle-outline
          span B
        v-col.pa-1(cols="3" @click="onChoose(2)")
          v-icon.ml-1(v-if="value === 2" color="green") mdi-check-circle
          v-icon.ml-1(v-if="value !== 2" color="#0000003d") mdi-checkbox-blank-circle-outline
          span C
        v-col.pa-1(cols="3" @click="onChoose(3)")
          v-icon.ml-1(v-if="value === 3" color="green") mdi-check-circle
          v-icon.ml-1(v-if="value !== 3" color="#0000003d") mdi-checkbox-blank-circle-outline
          span D
</template>

<script>
import {defineComponent} from "vue";

const MultipleChoice = defineComponent({
  props: ['no', 'value'],
  setup(props, {emit}) {
    const onChoose = (result) => {
      emit('on-choose', result)
    }

    return {
      onChoose
    }
  }
})

export default MultipleChoice
</script>

<style lang="sass" scoped>
.no
  color: red
  font-size: 17px
</style>