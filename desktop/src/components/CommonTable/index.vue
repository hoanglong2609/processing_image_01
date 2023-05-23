<template lang="pug">
  v-data-table.main(
    v-model="selected"
    :headers="headersRef"
    :items="itemsRef"
    hide-default-footer
    :item-key="itemKey ? itemKey : 'name'"
    :items-per-page="-1"
    class="elevation-1"
    :style="(maxWidth ? `max-width: ${maxWidth.toString()}px;` : '') + (width ? `width: ${width.toString()}px;` : '')"
    fixed-header
    @click:row="handleClick"
  )
    template(v-slot:header.data-table-select="{ props, on }")
      div.border-checkbox
        v-simple-checkbox(:value="props.value" v-on="on" color="primary")
    template(v-slot:item.name="{ item }")
      slot(name="name" :item="item")
        span {{item.name}}
    template(v-slot:item.role="{ item }")
      slot(name="role" :item="item")
        span {{item.role === 1 ? 'teacher' : 'student'}}
    template(v-slot:item.action="{ item }")
      slot(name="action" :item="item")
    template(v-for='(_, slot) of $scopedSlots' v-slot:[slot]='scope')
      slot(v-bind='scope', :name='slot')

</template>
<script>
import {defineComponent, onMounted, ref, watch} from 'vue'

const CommonTable = defineComponent({
  props: {
    headers: {
      type: Array,
      required: true
    },
    items: {
      type: Array,
      required: true
    },
    maxWidth: {
      type: Number,
      default: 1000,
      required: false
    },
    width: {
      type: Number,
      default: null,
      required: false
    },
    showSelect: {
      type: Boolean,
      default: false,
      required: false
    },
    itemKey: {
      type: String,
      required: false
    }
  },
  setup(props, {emit}) {
    const headersRef = ref([])
    const itemsRef = ref([])
    const selected = ref([])

    const handleClick = (row) => {
      emit('on-click', row)
    }

    const generateTable = () => {
      headersRef.value = props.headers
      itemsRef.value = props.items
    }

    onMounted(() => {
      generateTable()
    })
    watch(props, () => {
      generateTable()
    })
    watch(selected, () => {
      emit('on-select', selected)
    })
    return {
      selected,
      headersRef,
      itemsRef,
      handleClick
    }
  }
})

export default CommonTable
</script>

<style scoped lang="sass">
.main
  margin: 0 auto
.text-start
  padding: 0

</style>
