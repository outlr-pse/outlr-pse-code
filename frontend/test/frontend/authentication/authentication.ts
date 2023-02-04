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

describe('Logging in to an account registered and logged out of',  function () {
    test('registering and then logging in', async () => {
        const username = "SCH3LOM0"
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

    })

    test("registering with invalid username", async () => {

    })

    test("registering with username already taken", async () => {

    })

    test("logging in to registered account with wrong password", async () => {

    })

    test("logging in to account that is not registered", async () => {

    })

    test("logging out when not logged in", async () => {

    })
});