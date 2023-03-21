import axios from 'axios'
import * as config from '../config.json'

const axiosClient = axios.create({
  baseURL: config.API_URL
})

export default axiosClient
