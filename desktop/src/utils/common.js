import {api} from "@/plugins"
import Vue from "vue";


const objectToString = (object) => {
    let result = ''
    Object.keys(object).forEach(key => {
        result += `${key}=${object[key]}&`
    })
    return result
}


export const getData = async (listData = [], query = {}) => {
    const result = {
        subjects: null,
        users: null,
        scores: null
    }
    const querySubject = query?.subject ? objectToString(query.subject) : ''
    const queryUser = query?.user ? objectToString(query.user) : ''
    const queryScore = query?.score ? objectToString(query.score) : ''

    try {
        await Promise.all([
            listData.includes('user') ? api.get(`/user/?${queryUser}`).then(({data}) => result.users = data) : null,
            listData.includes('subject') ? api.get(`/subject/?${querySubject}`).then(({data}) => result.subjects = data) : null,
            listData.includes('score') ? api.get(`/score/?${queryScore}`).then(({data}) => result.scores = data) : null
        ])
    } catch (e) {
        Vue.$toast.error('get data failed')
    }

    return result
}


export const createData = async (endpoint, payload, showMsg= true) => {
    try {
        const {data} = await api.post(endpoint, payload)
        if (showMsg) Vue.$toast.success('create successful')
        return data
    } catch (e) {
        Vue.$toast.error('create failed')
    }
    return null
}


export const updateData = async (endpoint, id, data) => {
    try {
        await api.put(`${endpoint}${id}`, data)
        Vue.$toast.success('update successful')
    } catch (e) {
        this.$toast.error('update failed')
    }
}


export const deleteData = async (endpoint, id) => {
    try {
        await api.delete(`${endpoint}${id}`)
        Vue.$toast.success('delete successful')
    } catch (e) {
        console.log(e)
    }
}


export const readFile = (file) => {
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onloadend = () => resolve(reader.result)
  })
}