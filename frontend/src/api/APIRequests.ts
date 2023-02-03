import axios from 'axios'
import {authHeader} from "./DataRetrievalService";

export async  function sendLogout() : Promise<any>{
    /**
     * Sends request to back-end to delete/invalidate the access token provided
     * with the http request.
     */
    try {
        return axios.post('http://localhost:5000/user/logout',
            {},
            {headers: authHeader()})
    }
    catch (error) {
        return error
    }
}

export async function sendLoginData(username : string, password : string) : Promise<any>{
    /**
     * Sends data necessary for logging in to the back-end - Returns a promise,
     * which contains the access token and username in a user JSON, when logging in was
     * successful
     */
    try {
        return axios.post('http://localhost:5000/user/login',
            {username: username,password: password},
            {headers: authHeader()})
    }
    catch (error) {
        return error
    }
}

export async function sendRegisterData(username : string, password : string) : Promise<any> {
    /**
     * Sends data necessary for creation of an experiment to the back-end -
     * Returns a promise, which contains the access token and username in a user JSON, when
     * registering was successful
     */
    try {
        return axios.post('http://localhost:5000/user/register',
            {username: username,password: password},
            {headers: authHeader()})
    }
    catch (error) {
        return error
    }
}

export async function requestTokenIdentity() : Promise<any> {
    /**
     * This method sends a get-token-identity request to the backend receiving a user JSON
     * in a promise on success. The response, a promise, is returned
     */
    try {
        return axios.get('http://localhost:5000/user/get-token-identity',{headers: authHeader()})
    }
    catch(error) {
        return error
    }
}