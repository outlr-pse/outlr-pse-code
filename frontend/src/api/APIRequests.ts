import axios, {AxiosError} from 'axios'
import {authHeader} from "./DataRetrievalService";

export async  function sendLogout() : Promise<any>{
    try {
        const response = await axios.post('http://localhost:5000/user/logout',{}, {headers: authHeader()})
        return response
    }
    catch (error) {
        return error
    }
}

export async function sendLoginData(username : string, password : string) : Promise<any>{
    try {
        const response = await axios.post('http://localhost:5000/user/login', {username: username,password: password}, {headers: authHeader()})
        return response
    }
    catch (error) {
        return error
    }
}

export async function sendRegisterData(username : string, password : string) : Promise<any> {
    try {
        const response = await axios.post('http://localhost:5000/user/register', {username: username,password: password}, {headers: authHeader()})
        return response
    }
    catch (error) {
        return error
    }
}

export async function requestTokenIdentity() : Promise<any> {
    try {
        return await axios.get('http://localhost:5000/user/get-token-identity',{headers: authHeader()})
    }
    catch(error) {
        return error
    }
}