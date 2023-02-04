import {validatePassword, validateUsername} from "../../../src/api/AuthServices"

describe('validateData', () => {
    let validUsernames
    let invalidUsernames
    let invalidPasswords
    let validPasswords

    beforeAll( () => {

        validUsernames = [
            "salomo",
            "SCH3LOM0",
            "Ud0",
            "SuD0",
            "j_6",
            "H__",
            "H2Y2U8CI56W_A3SaH7_XA_6LBF_2_"
        ]

        invalidUsernames = [
            " ",
            "",
            null,
            "!io",
            "H1",
            "!!!",
            "ThisLooksValid02!",
            "*hilkdsfskdfkjlffjdkglöi28o3u4rlgh21",
            "XW>OM0Z4=4JR;O<=:/WBETFXXWVW4QP",
            "XW_OM0Z4_4JR_O____WBETFXXWVW4QP"
        ]

        validPasswords = [
            "s&1Hzk",
            "Heinz1_22",
            "Hallo&%1",
            "TestPasswordValid0!",
            "GoodPassword01&!",
            "%/HULIm21d"
        ]

        invalidPasswords = [
            "T&l?0",
            "78Hqh",
            null,
            "H&k____",
            " ",
            "  ",
            "1Hk777777",
            "1_hhhhhzuip",
            "1_HHHHHZUIP"
        ]
    })

    // USER VALIDATION
    test('valid usernames', () => {
        for (let username in validUsernames) {
            expect(validateUsername(username)).toEqual(true)
        }
    })

    test('should return false - invalid usernames', () => {
        for (let username in invalidUsernames) {
            expect(validateUsername(username)).toEqual(false)
        }
    })

    // PASSWORD VALIDATION
    test('password repeated does not equal actual password', () => {
        for(let i = 0; i < validPasswords.size - 1; i++) {
            expect(validatePassword(validPasswords[i], validPasswords[i+1])).toEqual(false)
        }
    })

    test('should return true - valid password', () => {
        for (let password in validPasswords) {
            expect(validatePassword(password, password)).toEqual(true)
        }
    });

    test('should return false - invalid password', () => {
        for (let password in invalidPasswords) {
            expect(validatePassword(password, password)).toEqual(false)
        }
    });
});