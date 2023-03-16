import axios from 'axios'

const axiosClient = axios.create({
  baseURL: 'http://127.0.0.1:1337/api'
})

export default axiosClient
