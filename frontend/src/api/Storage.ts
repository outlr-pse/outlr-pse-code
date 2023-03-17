import { MockStorage } from './MockStorage'

let storage: Storage

if (typeof localStorage !== 'undefined') {
  storage = localStorage
} else {
  storage = new MockStorage()
}

export default storage
