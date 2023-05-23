<template lang="pug">
  div
    common-table(
      :headers="headers"
      :items="items"
      @on-click="onClickNextIcon"
      :max-width="maxWidth"
    )
      template(v-slot:action="{item}")
        v-menu(
          v-if="user.role === 3"
          left
          offset-y
          min-width="9vw"
        )
          template(v-slot:activator='{on}')
            v-btn(v-on='on' icon @click="$emit('click-icon', item)")
              v-icon(medium) mdi-dots-vertical
          v-list
            v-list-item(v-for="(action, i) in actions" :key="i" link @click="$emit(action.action, item)")
              v-icon.pr-3(:color="action.color") {{ action.icon }}
              v-list-item-title {{ action.text }}

      template(v-for='(_, slot) of $scopedSlots' v-slot:[slot]='scope')
          slot(v-bind='scope', :name='slot')
</template>
<script>
import { defineComponent } from 'vue'
import CommonTable from '../CommonTable/index'

const JMasterItemList = defineComponent({
  props: {
    maxWidth: {
      type: Number,
      default: 1000,
      required: false
    },
    items: {
      type: Array,
      required: true
    },
    headers: {
      type: Array,
      required: true
    },
    actions: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  components: {
    CommonTable
  },
  setup(props, { emit }) {
    // Click to open unit of each group
    const user = JSON.parse(localStorage.getItem('user'))
    const onClickNextIcon = (item) => {
      emit('go-to-master-detail', item)
    }

    return {
      onClickNextIcon,
      user
    }
  }
})

export default JMasterItemList
</script>

<style scoped lang="sass">
.home
  width: 100%

.btn
  border: 0px

.link-text
  color: blue
  text-decoration: underline

::v-deep table > thead > tr > th > span
  font-size: 16px

::v-deep table > tbody > tr > td
  font-size: 16px !important
</style>
