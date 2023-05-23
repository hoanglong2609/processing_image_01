const headers = [
  {
    text: '',
    align: 'start',
    sortable: false,
    width: 5,
  },
  {
    text: 'name',
    sortable: false,
    value: 'name'
  },
  {
    text: '',
    align: 'right',
    sortable: false,
    value: 'action',
  }
]
const actions = [
  {
    id: 1,
    text: 'edit',
    icon: 'mdi-pencil',
    action: 'on-update',
    disabled: false,
    color: 'gray'
  },
  {
    id: 2,
    text: 'delete',
    icon: 'mdi-delete-empty',
    action: 'on-delete',
    disabled: false,
    color: 'red'
  }
]

export {headers, actions}