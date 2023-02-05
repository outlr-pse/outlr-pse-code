import {sendLoginData, sendLogout, sendRegisterData, storage} from "./APIRequests";
import store from "../store"
import {errorOther} from "./ErrorOther";
import {getIdentity} from "./DataRetrievalService";

export async function initialValidityCheck() {
    let identityJson = await getIdentity()

    if ("username" in identityJson) {
        await store.dispatch("auth/setAuthenticated", identityJson.username)
    }
}

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

    let passwordRegex = new RegExp("(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{6,})")
    return passwordRegex.test(password)
}

export async function login(username : string, password : string){
    /**
     * This method tries to log in using {@link sendLoginData}
     * the provided credentials to send a request to the API. It returns
     * the JSON, which either can be successful and then contains the user (especially the token)
     * or not successful containing an error JSON of a specific {@link ErrorType}. If the API responds with a success
     * JSON the token is stored in storage and the state of vuex is changed.
     *
     * @param username the username, the user provided
     * @param password the password, the user provided
     */
     try {
        const response = await sendLoginData(username, password)
        if (response.error != null) {
            return response
        }

        const userJson = response.data.user
        if (userJson == null) {
            return errorOther
        }

        storage.removeItem('access_token')
        storage.setItem('access_token', userJson.access_token)
        await store.dispatch("auth/setAuthenticated", userJson.username, userJson.access_token)
        return response.data
        }
    catch (error) {
        return errorOther
    }
}


export async function register(username : string, password : string){
    /**
     * This method tries to register a user in using {@link sendRegisterData}
     * the provided credentials to send a request to the API. It returns
     * the JSON, which either can be successful and then contains the user (especially the token)
     * or not successful containing an error JSON of a specific {@link ErrorType}. If the API responds with a success
     * JSON the token is stored in storage and the state of vuex is changed.
     *
     * @param username the username, the user provided
     * @param password the password, the user provided
     */
    try {
        const response = await sendRegisterData(username, password)
        if (response.error != null) {
            return response
        }

        const userJson = response.data.user
        if (userJson == null) {
            return errorOther
        }

        storage.removeItem('access_token')
        storage.setItem('access_token', userJson.access_token)
        await store.dispatch("auth/setAuthenticated", userJson.username, userJson.access_token)
        return response.data
        }
    catch (error) {
        return errorOther
    }
}

export async function logout() {
    /**
     * This method logs out a user using {@link sendLogout}
     * to request the deletion of the token on API side - it also removes
     * the current access token, which will be invalidated by API, from the local storage.
     * It returns the response JSON data.
     *
     * @param username the username, the user provided
     * @param password the password, the user provided
     */
    try {
            const response = await sendLogout()
            if (response.error != null) {
                return response
            }

            const userJson = response.data.user
            if (userJson == null) {
                return errorOther
            }

            if ("username" in userJson) {
                storage.removeItem("access_token")
                await store.dispatch("auth/unsetAuthenticated")
            }
            return response.data
        } catch (error) {
            return errorOther
        }
}
