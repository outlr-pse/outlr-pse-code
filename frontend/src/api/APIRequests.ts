import axios from 'axios'
import {authHeader} from "./DataRetrievalService";

export async  function sendLogout() : Promise<any>{
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
    try {
        return axios.get('http://localhost:5000/user/get-token-identity',{headers: authHeader()})
    }
    catch(error) {
        return error
    }
}