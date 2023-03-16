/**
 * @jest-environment jsdom
 */
import {errorOther} from "../../../src/api/ErrorOther";
import storage from "../../../src/api/Storage";
import {login, register} from "../../../src/api/AuthServices";
import store from "../../../src/store";

let mockError = false
let currentUsername = "Ud0"
jest.mock("../../../src/api/AxiosClient", () => {
    return {
        post: jest.fn().mockImplementation((url: string, data?: any, config?: any) => {
            switch (url) {
                case "/user/register":
                    if (data.username == null || data.password == null || mockError) {
                        throw new Error()
                    }
                    currentUsername = data.username
                    return {
                        data: {
                            username: data.username,
                            access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODkyMDU1MiwianRpIjoiOWRiZjUzZWItYmJlYi00NGU4LTg4ZGUtYmMwMTY2M2JkNTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjc4OTIwNTUyLCJleHAiOjE2Nzg5MjE0NTJ9.mW_UKL69SIR7NA60PFcVZxl3evPkVVYE8WCWA3rsr1k"
                        },
                        status: 200
            };
        case "/user/login":
            if (data.username) currentUsername = data.username
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
                        username: currentUsername,
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


describe("Tests DataRetrievalService", () => {
    test("Logging in when valid data passed is mocked", async () => {
        const username = "Ud0"
        const password = "Test01!"
        await login(username, password)
        expect(storage.getItem("access_token")).toBeDefined()
        expect(store.getters["auth/username"]).toEqual(username)
        expect(store.getters["auth/isAuthenticated"]).toEqual(true)

        await store.dispatch("auth/unsetAuthenticated")
        storage.clear()
        expect(store.getters["auth/username"]).not.toEqual(username)
        expect(store.getters["auth/isAuthenticated"]).not.toEqual(true)
    })
    test("Registering with valid data passed is mocked", async () => {
        const username = "Ud1"
        const password = "Test01!"
        await register(username, password)
        expect(storage.getItem("access_token")).toBeDefined()
        const usernameInStore = store.getters["auth/username"]
        const authState = store.getters["auth/isAuthenticated"]
        expect(usernameInStore).toEqual(username)
        expect(authState).toEqual(true)
    })

})