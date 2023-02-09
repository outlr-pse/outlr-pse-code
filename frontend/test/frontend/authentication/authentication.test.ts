/**
 * @jest-environment jsdom
 */

import {login, logout, register} from "../../../src/api/AuthServices";
import store from "../../../src/store";
import {axiosClient, requestTokenIdentity, storage} from "../../../src/api/APIRequests";

async function checkAuthenticationSuccessful(response: { error?: any; username?: any; access_token?: any;}, username: string) {
    expect(response.error).not.toBeDefined()

    expect(response.username).toBeDefined()
    expect(response.access_token).toBeDefined()
    expect(response.username).toBeDefined()


    expect(storage.getItem('access_token')).not.toBeNull()
    const tokenResponseJson = await requestTokenIdentity()
    expect(tokenResponseJson.username).toBeDefined()
    expect(tokenResponseJson.username).toEqual(username)

    // Vuex store auth states correctly set
    expect(store.getters["auth/username"]).toEqual(username)
    expect(store.getters["auth/isAuthenticated"]).toEqual(true)
}

async function notAuthenticated() {
    expect(store.getters["auth/username"]).toEqual("")
    expect(store.getters["auth/isAuthenticated"]).toEqual(false)
    expect(storage.getItem('access_token')).not.toBeDefined()
    expect((await requestTokenIdentity()).error).toBeDefined()
}

describe('Authentication', function () {

    beforeEach(() => {
            logout()
        }
    )

    test('registering', async () => {
        const response = register("schlomo12345", "TestPasswordValid0!")
        let response2 = response
    })

    test('test connection to backend', async () => {
        const response = axiosClient.get("/status")
        const data = (await response).data
        expect(data.status).toBeDefined()
        expect(data.status).toEqual("running")
    })


    test('registering and then logging in', async () => {
        const username = "SCH3LOM0TEST1"
        const password = "GoodPassword01&!"

        /*
        REGISTER with valid data - expectation: response with no error key but a user JSON
         */

        const response = await register(username, password)
        let response2 = response
        await checkAuthenticationSuccessful(response, username)

        /*
        LOGOUT
         */
        const response_logout = await logout()
        expect(response_logout).toEqual("")
        await notAuthenticated()
        /*
        LOGIN
         */
        const response_login = await login(username, password)
        await checkAuthenticationSuccessful(response_login, username)
    })

    test("registering with invalid username", async () => {
        const username = "H1"
        const password = "aG_4HfioiPerglioure9!"
        const response = await register(username, password)
        expect(response.error).toBeDefined()
        await notAuthenticated()
    })

    test("registering with invalid password", async () => {
        const username = "SCH3LOM0"
        const password = "abcd1"
        const response2 = await register(username, password)
        //const response = await register(username, password)
        expect(response2.error).toBeDefined()
        //TO-DO
        //expect(response.error.error).toEqual(ErrorType.UserManagementError)
        const response = await requestTokenIdentity()
        expect(response.error).toBeDefined()
        await notAuthenticated()
    })

    test("registering with username already taken", async () => {
        const username = "SCH3LOM0"
        const password = "s&1Hzk"
        const response = await register(username, password)
        await checkAuthenticationSuccessful(response, username)
        // Assumption: user with valid token can register more accounts
        const response_second_register = await register(username, password)
        expect(response_second_register.error).toBeDefined()
    })

    test("logging in to registered account with wrong password", async () => {
        const username = "not_registered"
        const password = "s&1Hzk"
        const response = await login(username, password)

        expect(response.error).toBeDefined()
        //TO-DO
        //expect(response.error.errorType).toEqual(ErrorType.UserManagementError)
    })

    test("logging in to account that is not registered", async () => {

        const username = "SCH3LOM0"
        const password = "s&1Hzk"

        const response_login = await login(username, password + "F")
        expect(response_login.error).toBeDefined()
        //TO-DO
        //expect(response_login.error.errorType).toEqual(ErrorType.UserManagementError)
    })

    test("logging out when not logged in", async () => {
        const response = await logout()
        expect(response.error).toBeDefined()
        expect(response.error).toBeDefined()
    })
});