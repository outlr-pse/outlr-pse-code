import axios, {AxiosError} from 'axios'
import {authHeader} from "./DataRetrievalService";
import {errorOther} from "./ErrorOther";

const axiosClient = axios.create({
    baseURL: 'http://127.0.0.1:1337/api'
});

export async  function sendLogout() : Promise<any>{
    /**
     * Sends request to back-end to delete/invalidate the access token provided
     * with the http request. In case of an error, the error JSON, as defined in backend, is returned.
     */
    try {
        return await axiosClient.post('/user/logout',
            {},
            {headers: authHeader()})
    }
    catch (error) {
        if (axios.isAxiosError(error)) {
                const serverError = error as AxiosError;
                if (serverError && serverError.response) {
                    return serverError.response.data;
                }
            }
        return errorOther
    }
}

export async function sendLoginData(username : string, password : string) : Promise<any>{
    /**
     * Sends data necessary for creation of an experiment to the back-end -
     * Returns a promise, which encapsulates a response containing the access token and username in a user JSON
     * in a data key, when logging in was successful.
     * In case of an error, the error JSON, as defined in backend, is returned.
     */
    try {
        return await axiosClient.post('/user/login',
            {username: username,password: password},
            {headers: authHeader()})
    }
    catch (error) {
        if (axios.isAxiosError(error)) {
                const serverError = error as AxiosError;
                if (serverError && serverError.response) {
                    return serverError.response.data;
                }
            }
        return errorOther
    }
}

export async function sendRegisterData(username : string, password : string) : Promise<any> {
    /**
     * Sends data necessary for creation of an experiment to the back-end -
     * Returns a promise, which encapsulates a response containing the access token and username in a user JSON
     * in a data key, when registering was successful.
     * In case of an error, the error JSON, as defined in backend, is returned.
     */
    try {
        return await axiosClient.post('/user/register',
            {username: username,password: password},
            {headers: authHeader()})
    }
    catch (error) {
        if (axios.isAxiosError(error)) {
                const serverError = error as AxiosError;
                if (serverError && serverError.response) {
                    return serverError.response.data;
                }
            }
        return errorOther
    }
}

export async function requestTokenIdentity() : Promise<any> {
    /**
     * This method sends a get-token-identity request to the backend receiving a response JSON containing the backends
     * actual JSON response in its data key as value. The actual JSON response contains a user JSON, which when a valid
     * token was passed contains user data, otherwise it is an empty JSON.
     */
    try {
        return await axiosClient.get('/user/get-token-identity',{headers: authHeader()})
    }
    catch(error) {
        if (axios.isAxiosError(error)) {
                const serverError = error as AxiosError;
                if (serverError && serverError.response) {
                    return serverError.response.data;
                }
            }
        return errorOther
    }
}