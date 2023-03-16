/**
 * @jest-environment jsdom
 */

import { getUrl, postUrl } from "../../../src/api/APIRequests";

jest.mock("../../../src/api/AxiosClient", () => {
  return {
    post: jest.fn().mockImplementation((url: string, data?: any) => {
        switch (url) {
            case "/user/register": return {
                data: {
                    username: data.username,
                    access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODkyMDU1MiwianRpIjoiOWRiZjUzZWItYmJlYi00NGU4LTg4ZGUtYmMwMTY2M2JkNTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjc4OTIwNTUyLCJleHAiOjE2Nzg5MjE0NTJ9.mW_UKL69SIR7NA60PFcVZxl3evPkVVYE8WCWA3rsr1k"
                    },
                status: 200
                }
            case "/user/login": return {
               data: {
                    username: data.username,
                    access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODkyMDU1MiwianRpIjoiOWRiZjUzZWItYmJlYi00NGU4LTg4ZGUtYmMwMTY2M2JkNTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjc4OTIwNTUyLCJleHAiOjE2Nzg5MjE0NTJ9.mW_UKL69SIR7NA60PFcVZxl3evPkVVYE8WCWA3rsr1k"
                    },
                status: 200
                }
            case '/user/logout': return {
                status: 200
            }
            case '/user/get-token-identity': return {
                    username: data.username,
                    access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODkyMDU1MiwianRpIjoiOWRiZjUzZWItYmJlYi00NGU4LTg4ZGUtYmMwMTY2M2JkNTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjc4OTIwNTUyLCJleHAiOjE2Nzg5MjE0NTJ9.mW_UKL69SIR7NA60PFcVZxl3evPkVVYE8WCWA3rsr1k"
            }
            //To-Do
        }
    }),
    get: jest.fn().mockImplementation((url: string, config?: any) => {
        switch (url) {
            case "/user/get-token-identity": return {
                data: {
                    username: config.headers,
                    access_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODkyMDU1MiwianRpIjoiOWRiZjUzZWItYmJlYi00NGU4LTg4ZGUtYmMwMTY2M2JkNTY2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjc4OTIwNTUyLCJleHAiOjE2Nzg5MjE0NTJ9.mW_UKL69SIR7NA60PFcVZxl3evPkVVYE8WCWA3rsr1k"
                    },
                status: 200
                }
            //To-Do
        }
    }),
  };
});

describe('API Requests test', () => {


    test("Logout when not logged in", async () => {
        const response = await postUrl()
        expect(response).toBe('/testing')
    })
})