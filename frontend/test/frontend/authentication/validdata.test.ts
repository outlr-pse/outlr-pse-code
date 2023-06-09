/**
 * @jest-environment jsdom
 */

import {validatePassword, validateUsername} from "../../../src/api/AuthServices"

describe('validateData', () => {
    let validUsernames: Array<string>
    let invalidUsernames: Array<string>
    let invalidPasswords: Array<string>
    let validPasswords: Array<string>

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
        validUsernames.forEach(val => {expect(validateUsername(val)).toEqual(true)})
    })

    test('should return false - invalid usernames', () => {
        invalidUsernames.forEach(val => {expect(validateUsername(val)).toEqual(false)})
    })

    // PASSWORD VALIDATION
    test.skip('password repeated does not equal actual password', () => {
        for(let i = 0; i < validPasswords.length - 1; i++) {
            expect(validatePassword(validPasswords[i])).toEqual(false)
        }
    })

    test('should return true - valid password', () => {
        validPasswords.forEach(val => {expect(validatePassword(val)).toEqual(true)})
    });

    test('should return false - invalid password', () => {
        invalidPasswords.forEach(val => {expect(validatePassword(val)).toEqual(false)})
    });
});