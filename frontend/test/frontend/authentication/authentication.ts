import {login, logout, register} from "../../../src/api/AuthServices";
import {getIdentity} from "../../../src/api/DataRetrievalService";
import store from "../../../src/store";
import {ErrorType} from "../../../src/models/error/ErrorType";

async function checkAuthenticationSuccessful(response, username){
        //TO-DO: find out if null or undefined
        expect(response.error).toBeNull()

        expect(response.user.username).not.toBeNull()
        expect(response.user.token).not.toBeNull()
        expect(response.user.username).not.toBeNull()
        expect(response.user.token).not.toBeNull()

        expect(localStorage.getItem('token')).not.toBeNull()
        expect(await getIdentity()).toEqual(username)

        // Vuex store auth states correctly set
        expect(store.getters["auth/username"]).toEqual(username)
        expect(store.getters["auth/isAuthenticated"]).toEqual(true)
}

async function notAuthenticated() {
        expect(store.getters["auth/username"]).toEqual("")
        expect(store.getters["auth/isAuthenticated"]).toEqual(false)
        expect(localStorage.getItem('token')).toBeNull()
        expect(await getIdentity()).toEqual("")
}

describe('Authentication',  function () {

    beforeEach(() => {
            logout()
        }
    )

    test('registering and then logging in', async () => {
        const username = "SCH3LOM0TEST1"
        const password = "GoodPassword01&!"

        /*
        REGISTER with valid data - expectation: response with no error key but a user JSON
         */
        const response = await register(username, password)
        await checkAuthenticationSuccessful(response, username)

        /*
        LOGOUT
         */
        const response_logout = await logout()
        expect(response_logout.token).not.toBeNull()
        expect(response_logout.error).toBeNull()
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
        expect(response.error).not.toBeNull()
        expect(response.error.errorType).toEqual(ErrorType.UserManagementError)
        await notAuthenticated()
    })

    test("registering with invalid password", async () => {
        const username = "SCH3LOM0"
        const password = "abcd1"
        const response = await register(username, password)
        expect(response.error).not.toBeNull()
        expect(response.error.errorType).toEqual(ErrorType.UserManagementError)
        expect(await getIdentity()).toEqual({})
        await notAuthenticated()
    })

    test("registering with username already taken", async () => {
        const username = "SCH3LOM0"
        const password = "s&1Hzk"
        const response = await register(username, password)
        await checkAuthenticationSuccessful(response, username)
        // Assumption: user with valid token can register more accounts
        const response_second_register = await register(username, password)
        expect(response_second_register.error).not.toBeNull()
        expect(response_second_register.error.errorType).toEqual(ErrorType.UserManagementError)
    })

    test("logging in to registered account with wrong password", async () => {
        const username = "not_registered"
        const password = "s&1Hzk"
        const response = await login(username, password)

        expect(response.error).not.toBeNull()
        expect(response.error.errorType).toEqual(ErrorType.UserManagementError)
    })

    test("logging in to account that is not registered", async () => {

        const username = "SCH3LOM0"
        const password = "s&1Hzk"

        const response_login = await login(username, password + "F")
        expect(response_login.error).not.toBeNull()
        expect(response_login.error.errorType).toEqual(ErrorType.UserManagementError)
    })

    test("logging out when not logged in", async () => {
        const response = await logout()
        expect(response.error).not.toBeNull()
        expect(response.error).not.toBeNull()
    })
});