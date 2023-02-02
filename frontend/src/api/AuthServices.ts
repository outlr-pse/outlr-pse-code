import {sendLoginData, sendLogout, sendRegisterData} from "./APIRequests";
import store from "../../../../Desktop/auth/store"
import axios, {AxiosError} from "axios";

function validateLoginData(username:string, password:string) : boolean {
    return true
}

function validateRegisterData(username:string, password:string, passwordRepeated:string) : boolean {
    return true
}

export async function login(username : string, password : string) : Promise<any> {
    if (validateLoginData(username, password)) {
        try {
            const response = await sendLoginData(username, password)
            const userJson = response.data.user
            if (userJson) {
                localStorage.setItem('token', userJson.token)
                await store.dispatch("auth/setAuthenticated", userJson.username, userJson.token)
            }
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const serverError = error as AxiosError;
                if (serverError && serverError.response) {
                    return serverError.response.data;
                }
            }
            return {message: "Something went wrong"}
        }
    }
}


export async function register(username : string, password : string, passwordRepeated : string){
    if (validateRegisterData(username, password, passwordRepeated)) {
        try {
            const response = await sendRegisterData(username, password)
            const userJson = response.data.user
            if (userJson) {
                console.log(userJson)
                localStorage.removeItem('token')
                localStorage.setItem('token', userJson.token)
                await store.dispatch("auth/setAuthenticated", userJson.username, userJson.token)
            }
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const serverError = error as AxiosError;
                if (serverError && serverError.response) {
                    return serverError.response.data;
                }
            }
            return {message: "Something went wrong"}
        }
    }
}

export async function logout() {
    try {
            const response = await sendLogout()
            const userJson = response.data.user
            if ("username" in userJson) {
                localStorage.removeItem("token")
                await store.dispatch("auth/unsetAuthenticated")
            }
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const serverError = error as AxiosError;
                if (serverError && serverError.response) {
                    return serverError.response.data;
                }
            }
            return {message: "Something went wrong"}
        }
}

