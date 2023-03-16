import storage from "./Storage"

export function authHeader (): any {
  /**
     * Generates the header used for sending the token provided with http requests to the backend. If
     * no token is in the local storage it is a empty JSON.
     */

  const token = storage.getItem('access_token')

  if (token != null) {
    return { Authorization: 'Bearer ' + token }
  }

  return {}
}
