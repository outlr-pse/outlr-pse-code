import axios, {AxiosError} from 'axios'
import {authHeader} from "./DataRetrievalService";
import {errorOther} from "./ErrorOther";
import {MockStorage} from "./MockStorage";
import {ODM} from "../models/odm/ODM";
import {Experiment} from "../models/experiment/Experiment";


export const axiosClient = axios.create({
    baseURL: 'http://127.0.0.1:1337/api'
});

export const storage = new MockStorage()

export async  function sendLogout() : Promise<any>{
    /**
     * Sends request to back-end to delete/invalidate the access token provided
     * with the http request. In case of an error, the error JSON, as defined in backend, is returned.
     */
    try {
        return await axiosClient.post('/user/logout',
            {},
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

export async function sendLoginData(username : string, password : string) : Promise<any>{
    /**
     * Sends data necessary for creation of an experiment to the back-end -
     * Returns a promise, which encapsulates a response containing the access token and username in a user JSON
     * in a data key, when logging in was successful.
     * In case of an error, the error JSON, as defined in backend, is returned.
     */
    try {
        return await axiosClient.post('/user/login',
            {username: username,password: password},
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

export async function sendRegisterData(username : string, password : string) : Promise<any> {
    /**
     * Sends data necessary for creation of an experiment to the back-end -
     * Returns a promise, which encapsulates a response containing the access token and username in a user JSON
     * in a data key, when registering was successful.
     * In case of an error, the error JSON, as defined in backend, is returned.
     */
    try {
        return await axiosClient.post('/user/register',
            {username: username,password: password},
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

export async function requestTokenIdentity() : Promise<any> {
    /**
     * This method sends a get-token-identity request to the backend receiving a response JSON containing the backends
     * actual JSON response in its data key as value. The actual JSON response contains a user JSON, which when a valid
     * token was passed contains user data, otherwise it is an empty JSON.
     */
    try {
        return await axiosClient.get('/user/get-token-identity',{headers: authHeader()})
    }
    catch(error) {
        if (axios.isAxiosError(error)) {
                const serverError = error as AxiosError;
                if (serverError && serverError.response) {
                    return serverError.response.data;
                }
            }
        return errorOther
    }
}

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

export async function requestAllExperiments() : Promise<any>{
    let experiments:Experiment[] = []
    experiments.push(Experiment.fromJSON("{\"id\":5,\"name\":\"AExampleExperiment\",\"dataset_name\":\"5TestDataset\",\"odm\":{\"name\":\"1COPOD\",\"hyper_parameters\":[{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":true},{\"name\":\"n_jobs\",\"type\":\"integer\",\"optional\":true}]},\"param_values\":{\"contamination\":0.1,\"n_jobs\":-1},\"experiment_result\":{\"id\":4,\"running\":false,\"accuracy\":0.1,\"execution_date\":\"2019-01-01T00:00:00Z\",\"execution_time\":900}}"))
    experiments.push(Experiment.fromJSON("{\"id\":51,\"name\":\"BExampleExperiment3\",\"dataset_name\":\"4TestDataset2\",\"odm\":{\"name\":\"10HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1},\"experiment_result\":{\"id\":23,\"running\":false,\"accuracy\":0.97,\"execution_date\":\"2023-01-27T00:20:17.102Z\",\"execution_time\":20}}"))
    experiments.push(Experiment.fromJSON("{\"id\":51,\"name\":\"CxampleExperiment4\",\"dataset_name\":\"6TestDataset2\",\"odm\":{\"name\":\"3HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1},\"experiment_result\":{\"id\":23,\"running\":false,\"accuracy\":0.97,\"execution_date\":\"2023-01-27T00:20:17.102Z\",\"execution_time\":20}}"))
    experiments.push(Experiment.fromJSON("{\"id\":51,\"name\":\"DExampleExperiment4\",\"dataset_name\":\"1TestDataset2\",\"odm\":{\"name\":\"7HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1},\"experiment_result\":{\"id\":23,\"running\":false,\"accuracy\":0.97,\"execution_date\":\"2023-01-27T00:20:17.102Z\",\"execution_time\":20}}"))
    experiments.push(Experiment.fromJSON("{\"id\":51,\"name\":\"EExampleExperiment4\",\"dataset_name\":\"2TestDataset2\",\"odm\":{\"name\":\"11HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1},\"experiment_result\":{\"id\":23,\"running\":false,\"accuracy\":0.97,\"execution_date\":\"2023-01-27T00:20:17.102Z\",\"execution_time\":20}}"))
    experiments.push(Experiment.fromJSON("{\"id\":51,\"name\":\"FExampleExperiment4\",\"dataset_name\":\"7TestDataset2\",\"odm\":{\"name\":\"62HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1},\"experiment_result\":{\"id\":23,\"running\":false,\"accuracy\":0.97,\"execution_date\":\"2023-01-27T00:20:17.102Z\",\"execution_time\":20}}"))
    experiments.push(Experiment.fromJSON("{\"id\":51,\"name\":\"GExampleExperiment4\",\"dataset_name\":\"12TestDataset2\",\"odm\":{\"name\":\"9HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1},\"experiment_result\":{\"id\":23,\"running\":false,\"accuracy\":0.97,\"execution_date\":\"2023-01-27T00:20:17.102Z\",\"execution_time\":20}}"))
    experiments.push(Experiment.fromJSON("{\"id\":51,\"name\":\"HExampleExperiment4\",\"dataset_name\":\"3TestDataset2\",\"odm\":{\"name\":\"5HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1},\"experiment_result\":{\"id\":23,\"running\":false,\"accuracy\":0.97,\"execution_date\":\"2023-01-27T00:20:17.102Z\",\"execution_time\":20}}"))
    experiments.push(Experiment.fromJSON("{\"id\":51,\"name\":\"IExampleExperiment4\",\"dataset_name\":\"9TestDataset2\",\"odm\":{\"name\":\"2HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1},\"experiment_result\":{\"id\":23,\"running\":false,\"accuracy\":0.97,\"execution_date\":\"2023-01-27T00:20:17.102Z\",\"execution_time\":20}}"))
    experiments.push(Experiment.fromJSON("{\"id\":51,\"name\":\"JExampleExperiment4\",\"dataset_name\":\"8TestDataset2\",\"odm\":{\"name\":\"4HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1},\"experiment_result\":{\"id\":23,\"running\":false,\"accuracy\":0.97,\"execution_date\":\"2023-01-27T00:20:17.102Z\",\"execution_time\":20}}"))
    experiments.push(Experiment.fromJSON("{\"id\":51,\"name\":\"KExampleExperiment4\",\"dataset_name\":\"10TestDataset2\",\"odm\":{\"name\":\"8HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1},\"experiment_result\":{\"id\":23,\"running\":false,\"accuracy\":0.97,\"execution_date\":\"2023-01-27T00:20:17.102Z\",\"execution_time\":20}}"))
    experiments.push(Experiment.fromJSON("{\"id\":51,\"name\":\"LExampleExperiment4\",\"dataset_name\":\"11TestDataset2\",\"odm\":{\"name\":\"12HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1}}"))
    return experiments;
}