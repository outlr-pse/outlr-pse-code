import {requestTokenIdentity} from "./APIRequests";
import axios, {AxiosError} from "axios";
import {errorOther} from "./ErrorOther";

export async function getIdentity() : Promise<any> {
    /**
     * Retrieves the identity of a token by handling {@link requestTokenIdentity} promise.
     * It returns either the user JSON, when token is valid containg username and token key, when not valid an empty
     * JSON. If an actual error occurs an error JSON is returned. The return values are encapsulated in a Promise.
     */
    try {
        const response = await requestTokenIdentity()
        return response.data.user
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
export function authHeader() {
    /**
     * Generates the header used for sending the token provided with http requests to the backend. If
     * no token is in the local storage it is a empty JSON.
     */

    let token = localStorage.getItem('token')

    if (token != null) {
        return {Authorization: 'Bearer ' + token}
    }

    return {}

}
