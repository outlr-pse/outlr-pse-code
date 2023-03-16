/**
 * @jest-environment jsdom
 */

import { getUrl, postUrl } from "../../../src/api/APIRequests";
import axios from "axios";
import { errorOther } from "../../../src/api/ErrorOther";

jest.mock("../../../src/api/AxiosClient", () => {
    return {
        post: jest.fn().mockImplementation((url: string, data?: any) => {
            switch (url) {
                case "/user/register":
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
                    return {
                        status: 200
                    };
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
        }),
        get: jest.fn().mockImplementation((url: string, config?: any) => {
            switch (url) {
                case "/user/get-token-identity":
                    return {
                        data: {
                            username: config.headers,
                            access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODkyMDU1MiwianRpIjoiOWRiZjUzZWItYmJlYi00NGU4LTg4ZGUtYmMwMTY2M2JkNTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjc4OTIwNTUyLCJleHAiOjE2Nzg5MjE0NTJ9.mW_UKL69SIR7NA60PFcVZxl3evPkVVYE8WCWA3rsr1k"
                        },
                        status: 200
                    };
                case "/odm/get-all":
                    return {};
                case "/experiment/get-all":
                    return {};
                default:
                    if (url.includes("/experiment/get-result/")) {
                        return {
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
                        }
                            ;
                    } else if (url.includes("/odm/get-parameters/")) {
                        return [
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
                        ];
                    }
                    return errorOther;
            }
        })
    };
});

describe("API Requests test", () => {
    test("Logout when not logged in", async () => {
        const response_test = await axios.get("http://127.0.0.1:1337/api/status");
        const response = await postUrl();
        expect(response).toBe("/testing");
    });
});