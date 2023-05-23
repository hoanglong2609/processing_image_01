import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:2100'
})

export default api