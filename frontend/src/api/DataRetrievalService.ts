import {requestTokenIdentity} from "./APIRequests";
import axios, {AxiosError} from "axios";

export async function getIdentity() : Promise<any> {
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
        return {message : "Something went wrong"}
    }
}
export function authHeader() {

    let token = localStorage.getItem('token')

    if (token != null) {
        return {Authorization: 'Bearer ' + token}
    }

    return {}

}
