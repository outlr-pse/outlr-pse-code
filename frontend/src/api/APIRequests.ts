import axios, { type AxiosError } from 'axios'
import { authHeader } from './DataRetrievalService'
import { errorOther } from './ErrorOther'
import { type Experiment } from '../models/experiment/Experiment'
import axiosClient from './AxiosClient'

export async function sendLogout (): Promise<any> {
  /**
     * Sends request to back-end to delete/invalidate the access token provided
     * with the http request. In case of an error, the error JSON, as defined in backend, is returned.
     */
  try {
    return await axiosClient.post('/user/logout',
      {},
      { headers: authHeader() })
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverError = error as AxiosError
      if (serverError?.response != null) {
        return serverError.response.data
      }
    }
    return errorOther
  }
}

export async function sendLoginData (username: string, password: string): Promise<any> {
  /**
     * Sends data necessary for creation of an experiment to the back-end -
     * Returns a promise, which encapsulates a response containing the access token and username in a user JSON
     * in a data key, when logging in was successful.
     * In case of an error, the error JSON, as defined in backend, is returned.
     */
  try {
    return await axiosClient.post('/user/login',
      { username, password },
      { headers: authHeader() })
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverError = error as AxiosError
      if (serverError?.response != null) {
        return serverError.response.data
      }
    }
    return errorOther
  }
}

export async function sendRegisterData (username: string, password: string): Promise<any> {
  /**
     * Sends data necessary for creation of an experiment to the back-end -
     * Returns a promise, which encapsulates a response containing the access token and username in a user JSON
     * in a data key, when registering was successful.
     * In case of an error, the error JSON, as defined in backend, is returned.
     */
  try {
    return await axiosClient.post('/user/register',
      { username, password },
      { headers: authHeader() })
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverError = error as AxiosError
      if (serverError?.response != null) {
        return serverError.response.data
      }
    }
    return errorOther
  }
}

export async function requestTokenIdentity (): Promise<any> {
  /**
     * This method sends a get-token-identity request to the backend receiving a response JSON containing the backends
     * actual JSON response in its data key as value. The actual JSON response contains a user JSON, which when a valid
     * token was passed contains user data, otherwise it is an empty JSON.
     */
  try {
    return (await axiosClient.get('/user/get-token-identity', { headers: authHeader() })).data
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverError = error as AxiosError
      if (serverError?.response != null) {
        return serverError.response.data
      }
    }
    return errorOther
  }
}

export async function sendExperiment (experiment: Experiment): Promise<any> {
  /**
     * Sends the experiment creation data to the back-end. Returns a promise, encapsulating
     * a JSON with info on whether sending the experiment creation was successful or not, then containing an error key
     */

  try {
    const formData = new FormData()
    formData.append('dataset', (experiment.dataset as Blob))
    formData.append('ground_truth', (experiment.groundTruth as Blob))
    await axiosClient.post('/experiment/upload-files', formData,
      { headers: authHeader() })

    return await axiosClient.post('/experiment/create', experiment.toJSON(),
      { headers: authHeader() })
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverError = error as AxiosError
      if (serverError?.response != null) {
        return serverError.response.data
      }
    }
    return errorOther
  }
}

export async function requestExperimentResult (experimentId: number): Promise<any> {
  /**
     * Sends request to back-end to respond with the result of the experiment with id = experimentId.
     */
  try {
    return await axiosClient.get(`/experiment/get-result/${experimentId}`, { headers: authHeader() })
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverError = error as AxiosError
      if (serverError?.response != null) {
        return serverError.response.data
      }
    }
    return errorOther
  }
}

export async function downloadExperiment (experiment: Experiment): Promise<any> {
  /**
     * Sends request to back-end to respond with the result of the experiment with id = experimentId.
     */
  await axiosClient.get(
    `/experiment/download-result/${experiment.id}`,
    {
      responseType: 'blob', // important
      headers: authHeader()
    }).then((response) => {
    // create file link in browser's memory
    const href = URL.createObjectURL(response.data)

    // create "a" HTML element with href to file & click
    const link = document.createElement('a')
    link.href = href
    console.log(response)
    const expName = experiment.name
    link.setAttribute('download', expName + '-result.csv') // or any other extension
    document.body.appendChild(link)
    link.click()

    // clean up "a" element & remove ObjectURL
    document.body.removeChild(link)
    URL.revokeObjectURL(href)
  })
}

export async function requestODMNames (): Promise<any> {
  /**
     * Sends request to back-end to respond with all ODMs
     */
  try {
    return await axiosClient.get('/odm/get-all', { headers: authHeader() })
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverError = error as AxiosError
      if (serverError?.response != null) {
        return serverError.response.data
      }
    }
    return errorOther
  }
}

export async function requestODM (odmId: number): Promise<any> {
  /**
     * Sends request to back-end to respond with the ODM with id = odmId
     */
  try {
    return await axiosClient.get(`/odm/get-parameters/${odmId}`, { headers: authHeader() })
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverError = error as AxiosError
      if (serverError?.response != null) {
        return serverError.response.data
      }
    }
    return errorOther
  }
}

export async function requestAllExperiments (): Promise<any> {
  /**
     * Sends request to back-end to respond with all experiments
     */
  try {
    return await axiosClient.get('/experiment/get-all', { headers: authHeader() })
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverError = error as AxiosError
      if (serverError?.response != null) {
        return serverError.response.data
      }
    }
    return errorOther
  }
}

export async function requestExperimentCount (): Promise<any> {
  /**
   * Sens request to back-end to respond with the number of experiments
   */
  try {
    return await axiosClient.get('/experiment/count', { headers: authHeader() })
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const serverError = error as AxiosError
      if (serverError?.response != null) {
        return serverError.response.data
      }
    }
    return errorOther
  }
}
