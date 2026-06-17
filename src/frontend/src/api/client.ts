import axios from 'axios'
import { BASE_PATH } from '@/config/runtime'

const client = axios.create({
  baseURL: `${BASE_PATH}/api`,
  timeout: 30000,
})

client.interceptors.response.use(
  r => r,
  err => {
    const msg = err.response?.data?.detail ?? err.message
    return Promise.reject(new Error(msg))
  }
)

export default client
