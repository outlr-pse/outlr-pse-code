/**
 * @jest-environment jsdom
 */
import { errorOther } from "../../../src/api/ErrorOther";
import {
    requestAllExperiments,
    requestExperimentResult,
    requestODM,
    requestODMNames,
    requestTokenIdentity,
    sendExperiment,
    sendLoginData,
    sendLogout,
    sendRegisterData
} from "../../../src/api/APIRequests";
import { authHeader } from "../../../src/api/DataRetrievalService";
import { Experiment } from "../../../src/models/experiment/Experiment";
import { ODM } from "../../../src/models/odm/ODM";
import {validateUsername} from "../../../src/api/AuthServices";
import axios from "axios";

jest.mock("../../../src/api/DataRetrievalService", () => ({
    authHeader: jest.fn(() => {
        return { Authorization: "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODkyMDU1MiwianRpIjoiOWRiZjUzZWItYmJlYi00NGU4LTg4ZGUtYmMwMTY2M2JkNTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjc4OTIwNTUyLCJleHAiOjE2Nzg5MjE0NTJ9.mW_UKL69SIR7NA60PFcVZxl3evPkVVYE8WCWA3rsr1k" };
    })
}));

let mockError = false;

jest.mock("../../../src/api/AxiosClient", () => {
    return {
        post: jest.fn().mockImplementation((url: string, data?: any, config?: any) => {
            switch (url) {
                case "/user/register":
                    if (data.username == null || data.password == null || mockError) {
                        throw new Error()
                    }
                    if (!validateUsername(data.username)) {
                        throw new axios.AxiosError('Request failed')
                    }
                    return {
                        data: {
                            username: data.username,
                            access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODkyMDU1MiwianRpIjoiOWRiZjUzZWItYmJlYi00NGU4LTg4ZGUtYmMwMTY2M2JkNTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjc4OTIwNTUyLCJleHAiOjE2Nzg5MjE0NTJ9.mW_UKL69SIR7NA60PFcVZxl3evPkVVYE8WCWA3rsr1k"
                        },
                        status: 200
            };
        case "/user/login":
            return {
                data: {
                    username: data.username,
                    access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODkyMDU1MiwianRpIjoiOWRiZjUzZWItYmJlYi00NGU4LTg4ZGUtYmMwMTY2M2JkNTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjc4OTIwNTUyLCJleHAiOjE2Nzg5MjE0NTJ9.mW_UKL69SIR7NA60PFcVZxl3evPkVVYE8WCWA3rsr1k"
                },
                status: 200
            };
        case "/user/logout":
            if (config.headers) {
                return {
                    status: 200
                };
            } else {
                return errorOther;
            }
        case "/user/get-token-identity":
            return {
                username: data.username,
                access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODkyMDU1MiwianRpIjoiOWRiZjUzZWItYmJlYi00NGU4LTg4ZGUtYmMwMTY2M2JkNTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjc4OTIwNTUyLCJleHAiOjE2Nzg5MjE0NTJ9.mW_UKL69SIR7NA60PFcVZxl3evPkVVYE8WCWA3rsr1k"
            };
        case "/experiment/upload-files":
            return {
                status: 200,
                data: "OK"
            };
        case "/experiment/create":
            return {
                status: 200,
                data: "OK"
            };
        default:
            return errorOther;
        }
    }
),
    get: jest.fn().mockImplementation((url: string, config?: any) => {
        switch (url) {
            case "/user/get-token-identity":
                return {
                    data: {
                        username: "Ud0",
                        access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODkyMDU1MiwianRpIjoiOWRiZjUzZWItYmJlYi00NGU4LTg4ZGUtYmMwMTY2M2JkNTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjc4OTIwNTUyLCJleHAiOjE2Nzg5MjE0NTJ9.mW_UKL69SIR7NA60PFcVZxl3evPkVVYE8WCWA3rsr1k"
                    },
                    status: 200
                };
            case "/odm/get-all":
                return {
                    data: [
                        {
                            "id": 2,
                            "name": "alad.ALAD"
                        },
                        {
                            "id": 3,
                            "name": "anogan.AnoGAN"
                        },
                        {
                            "id": 4,
                            "name": "cblof.CBLOF"
                        },
                        {
                            "id": 5,
                            "name": "cd.CD"
                        },
                        {
                            "id": 6,
                            "name": "cof.COF"
                        },
                        {
                            "id": 7,
                            "name": "copod.COPOD"
                        },
                        {
                            "id": 8,
                            "name": "ecod.ECOD"
                        },
                        {
                            "id": 9,
                            "name": "gmm.GMM"
                        },
                        {
                            "id": 10,
                            "name": "hbos.HBOS"
                        },
                        {
                            "id": 11,
                            "name": "iforest.IForest"
                        },
                        {
                            "id": 12,
                            "name": "inne.INNE"
                        },
                        {
                            "id": 13,
                            "name": "kde.KDE"
                        },
                        {
                            "id": 14,
                            "name": "knn.KNN"
                        },
                        {
                            "id": 15,
                            "name": "kpca.KPCA"
                        },
                        {
                            "id": 16,
                            "name": "lmdd.LMDD"
                        },
                        {
                            "id": 17,
                            "name": "loci.LOCI"
                        },
                        {
                            "id": 18,
                            "name": "loda.LODA"
                        },
                        {
                            "id": 19,
                            "name": "lof.LOF"
                        },
                        {
                            "id": 20,
                            "name": "lscp.LSCP"
                        },
                        {
                            "id": 21,
                            "name": "mad.MAD"
                        },
                        {
                            "id": 22,
                            "name": "mcd.MCD"
                        },
                        {
                            "id": 23,
                            "name": "mo_gaal.MO_GAAL"
                        },
                        {
                            "id": 24,
                            "name": "ocsvm.OCSVM"
                        },
                        {
                            "id": 25,
                            "name": "pca.PCA"
                        },
                        {
                            "id": 26,
                            "name": "rgraph.RGraph"
                        },
                        {
                            "id": 27,
                            "name": "rod.ROD"
                        },
                        {
                            "id": 28,
                            "name": "sampling.Sampling"
                        },
                        {
                            "id": 29,
                            "name": "so_gaal.SO_GAAL"
                        },
                        {
                            "id": 30,
                            "name": "sod.SOD"
                        },
                        {
                            "id": 31,
                            "name": "sos.SOS"
                        },
                        {
                            "id": 32,
                            "name": "suod.SUOD"
                        },
                        {
                            "id": 33,
                            "name": "vae.VAE"
                        },
                        {
                            "id": 34,
                            "name": "xgbod.XGBOD"
                        },
                        {
                            "id": 1,
                            "name": "abod.ABOD"
                        }
                    ],
                    status: 200
                };
            case "/experiment/get-all":
                return {
                    data: [
                        {
                            "dataset_name": "dataset.csv",
                            "error_json": null,
                            "experiment_result": {
                                "accuracy": 0.965,
                                "execution_date": "2023-03-16T10:59:25.332699",
                                "execution_time": 1577822,
                                "id": 5
                            },
                            "id": 5,
                            "name": "new Experiment",
                            "odm": {
                                "deprecated": false,
                                "hyper_parameters": [
                                    {
                                        "id": 826,
                                        "name": "contamination",
                                        "optional": true,
                                        "type": "<class 'float'>"
                                    },
                                    {
                                        "id": 827,
                                        "name": "n_neighbors",
                                        "optional": true,
                                        "type": "<class 'int'>"
                                    },
                                    {
                                        "id": 828,
                                        "name": "method",
                                        "optional": true,
                                        "type": "<class 'str'>"
                                    },
                                    {
                                        "id": 1101,
                                        "name": "contamination",
                                        "optional": true,
                                        "type": "<class 'float'>"
                                    },
                                    {
                                        "id": 1102,
                                        "name": "n_neighbors",
                                        "optional": true,
                                        "type": "<class 'int'>"
                                    },
                                    {
                                        "id": 1103,
                                        "name": "method",
                                        "optional": true,
                                        "type": "<class 'str'>"
                                    }
                                ],
                                "id": 1,
                                "name": "abod.ABOD"
                            },
                            "odm_params": {
                                "method": "fast"
                            }
                        }
                    ],
                    status: 200
                };
            default:
                if (url.includes("/experiment/get-result/")) {
                    return {
                        data: {
                            "dataset_name": "dataset.csv",
                            "error_json": null,
                            "experiment_result": {
                                "accuracy": 0.975,
                                "execution_date": "2023-03-16T10:33:42.831393",
                                "execution_time": 1002948,
                                "id": 2,
                                "result_space": {
                                    "columns": [],
                                    "id": 6,
                                    "name": "result",
                                    "outliers": [
                                        189,
                                        181,
                                        190,
                                        182,
                                        187,
                                        197,
                                        183,
                                        188,
                                        198,
                                        195,
                                        191,
                                        185,
                                        186,
                                        194,
                                        180
                                    ],
                                    "roc_curve": null
                                }
                            },
                            "id": 2,
                            "name": "new Experiment",
                            "odm": {
                                "deprecated": false,
                                "hyper_parameters": [
                                    {
                                        "id": 826,
                                        "name": "contamination",
                                        "optional": true,
                                        "type": "<class 'float'>"
                                    },
                                    {
                                        "id": 827,
                                        "name": "n_neighbors",
                                        "optional": true,
                                        "type": "<class 'int'>"
                                    },
                                    {
                                        "id": 828,
                                        "name": "method",
                                        "optional": true,
                                        "type": "<class 'str'>"
                                    },
                                    {
                                        "id": 1101,
                                        "name": "contamination",
                                        "optional": true,
                                        "type": "<class 'float'>"
                                    },
                                    {
                                        "id": 1102,
                                        "name": "n_neighbors",
                                        "optional": true,
                                        "type": "<class 'int'>"
                                    },
                                    {
                                        "id": 1103,
                                        "name": "method",
                                        "optional": true,
                                        "type": "<class 'str'>"
                                    }
                                ],
                                "id": 1,
                                "name": "abod.ABOD"
                            },
                            "odm_params": {
                                "method": "fast"
                            },
                            "subspace_logic": {
                                "operation": {
                                    "operands": [
                                        {
                                            "literal": {
                                                "subspace": {
                                                    "columns": [
                                                        0
                                                    ],
                                                    "id": 3,
                                                    "name": null,
                                                    "outliers": [
                                                        189,
                                                        181,
                                                        190,
                                                        184,
                                                        182,
                                                        196,
                                                        187,
                                                        197,
                                                        147,
                                                        183,
                                                        188,
                                                        198,
                                                        195,
                                                        191,
                                                        185,
                                                        113,
                                                        186,
                                                        194,
                                                        48,
                                                        180
                                                    ],
                                                    "roc_curve": null
                                                }
                                            }
                                        },
                                        {
                                            "operation": {
                                                "operands": [
                                                    {
                                                        "literal": {
                                                            "subspace": {
                                                                "columns": [
                                                                    1
                                                                ],
                                                                "id": 4,
                                                                "name": null,
                                                                "outliers": [
                                                                    192,
                                                                    189,
                                                                    193,
                                                                    181,
                                                                    190,
                                                                    199,
                                                                    182,
                                                                    16,
                                                                    187,
                                                                    197,
                                                                    188,
                                                                    198,
                                                                    195,
                                                                    191,
                                                                    33,
                                                                    186,
                                                                    101,
                                                                    194,
                                                                    174,
                                                                    180
                                                                ],
                                                                "roc_curve": null
                                                            }
                                                        }
                                                    },
                                                    {
                                                        "literal": {
                                                            "subspace": {
                                                                "columns": [
                                                                    0,
                                                                    1
                                                                ],
                                                                "id": 5,
                                                                "name": null,
                                                                "outliers": [
                                                                    192,
                                                                    189,
                                                                    193,
                                                                    181,
                                                                    190,
                                                                    199,
                                                                    182,
                                                                    187,
                                                                    197,
                                                                    183,
                                                                    188,
                                                                    198,
                                                                    195,
                                                                    191,
                                                                    185,
                                                                    107,
                                                                    186,
                                                                    194,
                                                                    174,
                                                                    180
                                                                ],
                                                                "roc_curve": null
                                                            }
                                                        }
                                                    }
                                                ],
                                                "operator": "or"
                                            }
                                        }
                                    ],
                                    "operator": "and"
                                }
                            }

                        },
                        status: 200
                    };
                } else if (url.includes("/odm/get-parameters/")) {
                    return {
                        data: [
                            {
                                "id": 364,
                                "name": "contamination",
                                "optional": true,
                                "type": "<class 'float'>"
                            },
                            {
                                "id": 365,
                                "name": "bandwidth",
                                "optional": true,
                                "type": "<class 'float'>"
                            },
                            {
                                "id": 366,
                                "name": "algorithm",
                                "optional": true,
                                "type": "<class 'str'>"
                            },
                            {
                                "id": 367,
                                "name": "leaf_size",
                                "optional": true,
                                "type": "<class 'int'>"
                            },
                            {
                                "id": 368,
                                "name": "metric",
                                "optional": true,
                                "type": "<class 'str'>"
                            },
                            {
                                "id": 369,
                                "name": "metric_params",
                                "optional": true,
                                "type": "<class 'NoneType'>"
                            }
                        ],
                        status: 200
                    };
                }
                return errorOther;
        }
    })
};
})
;

describe("API Requests test", () => {
    test("sendLoginData test", async () => {
        const username = "Ud0";
        const password = "Test01!";
        const response = await sendLoginData(username, password);
        expect(response.data).toBeDefined();
        expect(response.data.username).toBeDefined();
        expect(response.data.username).toEqual(username);
    });
    test("sendRegisterData test", async () => {
        const username = "Ud0";
        const password = "Test01!";
        const response = await sendRegisterData(username, password);
        expect(response.data).toBeDefined();
        expect(response.data.username).toBeDefined();
        expect(response.data.username).toEqual(username);
    });
    test("sendRegisterData no success test", async () => {
        mockError = true;
        const username = "Ud0";
        const password = "Test01!";
        let response
        try {
            response = await sendRegisterData(username, password);
        }
        catch(error) {
            response = error
        }
        expect(response.status).not.toEqual(200)
        expect(response.error).toBeDefined()
        expect(response.message).toBeDefined()
        mockError = false;
    });
    test("sendRegisterData but no valid username provided", async () => {
        const username = "Ud";
        const password = "Test01&"
        let response
        try {
            response = await sendRegisterData(username, password);
        } catch (error) {
            response = error
        }
        expect(response.status).not.toEqual(200)
        expect(response.error).toBeDefined()
        expect(response.message).toBeDefined()
    })
    test("sendLogout test", async () => {
        const response = await sendLogout();
        expect(response.status).toEqual(200);
    });
    test("authHeader now returns a header with access token no matter what since mocked", () => {
        const response = authHeader();
        expect(response.Authorization).toBeDefined();
    });
    test("requestTokenIdentity mock test", async () => {
        const responseData = await requestTokenIdentity();
        expect(responseData).toBeDefined();
        expect(responseData.username).toBeDefined();
        expect(responseData.access_token).toBeDefined();
    });
    test("sendExperiment mock test", async () => {
        const response = await sendExperiment(new Experiment("", "", null, null, new ODM(1, "", [])));
        expect(response.data).toBeDefined();
        expect(response.data).toEqual("OK");
        expect(response.status).toEqual(200);
    });
    test("Request Experiment result", async () => {
        const response = await requestExperimentResult(3);
        expect(response.status).toEqual(200);
        expect(response.data).toBeDefined();
        expect(response.data.id).toBeDefined();
        expect(response.data.name).toBeDefined();
        expect(response.data.dataset_name).toBeDefined();
        expect(response.data.odm).toBeDefined();
        expect(response.data.odm_params).toBeDefined();
        expect(response.data.subspace_logic).toBeDefined();
        expect(response.data.experiment_result).toBeDefined();
        expect(response.data.error_json).toBeDefined();
    });
    test("Request Experiment result", async () => {
        const response = await requestExperimentResult(3);
        expect(response.status).toEqual(200);
        expect(response.data).toBeDefined();
        expect(response.data.id).toBeDefined();
        expect(response.data.name).toBeDefined();
        expect(response.data.dataset_name).toBeDefined();
        expect(response.data.odm).toBeDefined();
        expect(response.data.odm_params).toBeDefined();
        expect(response.data.subspace_logic).toBeDefined();
        expect(response.data.experiment_result).toBeDefined();
        expect(response.data.error_json).toBeDefined();
    });
    test("Request ODM names result", async () => {
        const response = await requestODMNames();
        expect(response.status).toEqual(200);
        expect(response.data).toBeDefined();
        for (const [key, value] of Object.entries(response.data)) {
            // @ts-ignore
            expect(Object.keys(value).length).toBeDefined();
            // @ts-ignore
            expect(Object.keys(value).length).toEqual(2);
            // @ts-ignore
            expect(value.id).toBeDefined();
            // @ts-ignore
            expect(value.name).toBeDefined();
        }
    });
    test("Request ODM", async () => {
        const response = await requestODM(2);
        expect(response.status).toEqual(200);
        expect(response.data).toBeDefined();
        for (const [key, value] of Object.entries(response.data)) {
            // @ts-ignore
            expect(Object.keys(value).length).toBeDefined();
            // @ts-ignore
            expect(Object.keys(value).length).toEqual(4);
            // @ts-ignore
            expect(value.id).toBeDefined();
            // @ts-ignore
            expect(value.name).toBeDefined();
            // @ts-ignore
            expect(value.optional).toBeDefined();
            // @ts-ignore
            expect(value.type).toBeDefined();
        }
    });
    test("Request all experiments", async () => {
        const response = await requestAllExperiments();
        expect(response.status).toEqual(200);
        expect(response.data).toBeDefined();
        for (const [key, value] of Object.entries(response.data)) {
            // @ts-ignore
            expect(value.id).toBeDefined();
            // @ts-ignore
            expect(value.name).toBeDefined();
            // @ts-ignore
            expect(value.dataset_name).toBeDefined();
            // @ts-ignore
            expect(value.odm).toBeDefined();
            // @ts-ignore
            expect(value.odm_params).toBeDefined();
            // @ts-ignore
            expect(value.experiment_result).toBeDefined();
            // @ts-ignore
            expect(value.error_json).toBeDefined();
        }
    });
});