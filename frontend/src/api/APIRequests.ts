import axios, {AxiosError} from 'axios'
import {authHeader} from "./DataRetrievalService";
import {errorOther} from "./ErrorOther";
import {MockStorage} from "./MockStorage";
import {ODM} from "../models/odm/ODM";
import {Experiment} from "../models/experiment/Experiment";

export const axiosClient = axios.create({
    baseURL: 'http://127.0.0.1:5000/api'
});
export const storage = new MockStorage()

export async function sendDataset(dataset:File) : Promise<any>{
    /**
     * Sends request to back-end to validate the dataset passed in form data of the http request.
     * In case of an error, the error JSON, as defined in backend, is returned.
     */
    try {
        const formData = new FormData()
        formData.append('file', dataset, dataset.name)
        return await axiosClient.post('/experiment/validate-dataset', formData,
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

export async function sendGroundTruth(groundTruth:File) : Promise<any>{
    /**
     * Sends request to back-end to validate the ground truth passed in form data of the http request.
     * In case of an error, the error JSON, as defined in backend, is returned.
     */
    try {
        const formData = new FormData()
        formData.append('file', groundTruth, groundTruth.name)
        return await axiosClient.post('/experiment/validate-ground-truth', formData,
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

export async function sendODM(odm:ODM) : Promise<any>{
    /**
     * Sends the selected ODM to the back-end. Returns a promise, encapsulating
     * a JSON with info on whether sending the ODM was successful or not, then containing an error key
     */
    try {
        return await axiosClient.post('/experiment/validate-ground-truth', {odm:odm.toJSON()},
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

export async function sendExperiment(experiment:Experiment) : Promise<any>{
    /**
     * Sends the experiment creation data to the back-end. Returns a promise, encapsulating
     * a JSON with info on whether sending the experiment creation was successful or not, then containing an error key
     */
    try {
        return await axiosClient.post('/experiment/create', {experiment:experiment.toJSON()},
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

export async function requestExperimentResult(experimentId:number) : Promise<any>{
    /**
     * Sends request to back-end to respond with the result of the experiment with id = experimentId.
     */
    try {
        return await axiosClient.get(`/experiment/get-result/${experimentId}`, {headers: authHeader()})
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

export async function requestODMNames() : Promise<any>{
    /**
     * Sends request to back-end to respond with all ODMs
     */
    try {
        return await axiosClient.get('/odm/get-all', {headers: authHeader()})
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

export async function requestODM(odmId:number) : Promise<any>{
    /**
     * Sends request to back-end to respond with the ODM with id = odmId
     */
    try {
        return await axiosClient.get(`/odm/get-parameters/${odmId}`, {headers: authHeader()})
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
