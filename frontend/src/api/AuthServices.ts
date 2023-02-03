import {sendLoginData, sendLogout, sendRegisterData} from "./APIRequests";
import store from "../store"
import axios, {AxiosError} from "axios";

export function validateUsername(username : string) : boolean {
    /**
     * validate the login data and return either true, when username is valid, or false, when username is not valid
     *
     * A username is valid, if:
     * - It starts with a letter from the alphabet
     * - All other characters can be alphabets, numbers or an underscore
     * - the username should not be shorter than 3 letters and not longer than 30 characters
     *
     * @param username the username, the user provided
     */
    if (username == null) {
        return false
    }
    let usernameRegex = new RegExp("^[A-Za-z][A-Za-z0-9_]{2,29}$")
    return usernameRegex.test(username)
}

export function validatePassword(password:string, passwordRepeated:string) {
    /**
     * validate the password and return either true, when password is valid, or false, when password is not valid - only
     * if password equals passwordRepeated
     *
     * A password is valid, if:
     * - the minimum number of characters is 6
     * - at least one digit must be included
     * - at least one uppercase letter must be included
     * - at least one lowercase letter must be included
     * - at least one special character
     *
     * @param password the password, the user provided
     */
    if (password == null || passwordRepeated == null || password != passwordRepeated) {
        return false
    }

    let passwordRegex = new RegExp("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})")
    return passwordRegex.test(password)
}

export async function login(username : string, password : string){
    /**
     * This method tries to log in using {@link sendLoginData}
     * the provided credentials to send a request to the API. It returns
     * the JSON, which either can be successful and then contains the user (especially the token)
     * or not successful containing an error JSON of a specific {@link ErrorType}.
     *
     * @param username the username, the user provided
     * @param password the password, the user provided
     */
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
    /**
     * This method tries to register a user in using {@link sendRegisterData}
     * the provided credentials to send a request to the API. It returns
     * the JSON, which either can be successful and then contains the user (especially the token)
     * or not successful containing an error JSON of a specific {@link ErrorType}.
     *
     * @param username the username, the user provided
     * @param password the password, the user provided
     */
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
    /**
     * This method logs out a user using {@link sendLogout}
     * request to request the token deletion of the token on API side - it also removes
     * the current access token, which will be invalidated, from the local storage.
     * It returns the response JSON data.
     *
     * @param username the username, the user provided
     * @param password the password, the user provided
     */
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

