import {sendLoginData, sendLogout, sendRegisterData} from "./APIRequests";
import store from "../store"
import axios, {AxiosError} from "axios";

function validateLoginData(username:string, password:string) {
    /**
     * validate the login data and return either true, when data is valid, or false, when data is not valid
     *
     * A username is valid, if:
     * - It starts with a letter from the alphabet
     * - All other characters can be alphabets, numbers or an underscore
     * - the username should not be shorter than 3 letters and not longer than 30 characters
     *
     * A password is valid, if:
     * - the minimum number of characters
     *
     * @param username the username, the user provided
     * @param password the password, the user provided
     */
    let usernameRegex = "^[A-Za-z][A-Za-z0-9_]{2,29}$"
}

function validateRegisterData(username:string, password:string, passwordRepeated:string) : boolean {
    return true
}

export async function login(username : string, password : string){
        try {
            const response = await sendLoginData(username, password)
            const userJson = response.data.user
            if (userJson) {
                localStorage.setItem('token', userJson.token)
                await store.dispatch("auth/setAuthenticated", userJson.username, userJson.token)
            }
            return response.data
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


export async function register(username : string, password : string){
        try {
            const response = await sendRegisterData(username, password)
            const userJson = response.data.user
            if (userJson) {
                localStorage.removeItem('token')
                localStorage.setItem('token', userJson.token)
                await store.dispatch("auth/setAuthenticated", userJson.username, userJson.token)
            }
            return response.data
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

export async function logout() {
    try {
            const response = await sendLogout()
            const userJson = response.data.user
            if ("username" in userJson) {
                localStorage.removeItem("token")
                await store.dispatch("auth/unsetAuthenticated")
            }
            return response.data
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

