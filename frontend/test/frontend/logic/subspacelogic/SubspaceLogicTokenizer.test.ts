import {TokenType, tokenize} from '../../../../src/logic/subspacelogic/SubspaceLogicTokenizer'

describe("SubspaceLogicTokenizer", () => {

    it("Tokenize literal", () => {
        const literal = "[1,2,3]"
        const expected = [[TokenType.BeginLit, undefined], [TokenType.Cols, [1, 2, 3]], [TokenType.EndLit, undefined]]
        const actual = tokenize(literal)
        expect(actual).toEqual(expected)
    })

    it("Tokenize literal with spaces", () => {
        const literal = "[ 1 , 2 , 3 ]"
        const expected = [[TokenType.BeginLit, undefined], [TokenType.Cols, [1, 2, 3]], [TokenType.EndLit, undefined]]
        const actual = tokenize(literal)
        expect(actual).toEqual(expected)
    })

    it("Tokenize operation", () => {
        const literal1 = "[1,2,3]"
        const literal2 = "[4,5,6]"
        const operation = "(" + literal1 + " and " + literal2 + ")"

        const expectedLiteral1 = [
            [TokenType.BeginLit, undefined],
            [TokenType.Cols, [1, 2, 3]],
            [TokenType.EndLit, undefined]
        ]
        const expectedLiteral2 = [
            [TokenType.BeginLit, undefined],
            [TokenType.Cols, [4, 5, 6]],
            [TokenType.EndLit, undefined]
        ]
        const expected = [[TokenType.BeginScope, undefined], ...expectedLiteral1,
            [TokenType.Text, "and"], ...expectedLiteral2, [TokenType.EndScope, undefined]]
    })

    it("Tokenize operation with spaces", () => {
        const literal1 = "[ 1 , 2 , 3 ]"
        const literal2 = "[ 4 , 5 , 6 ]"
        const operation = "( " + literal1 + " and " + literal2 + " )"

        const expectedLiteral1 = [
            [TokenType.BeginLit, undefined],
            [TokenType.Cols, [1, 2, 3]],
            [TokenType.EndLit, undefined]
        ]
        const expectedLiteral2 = [
            [TokenType.BeginLit, undefined],
            [TokenType.Cols, [4, 5, 6]],
            [TokenType.EndLit, undefined]
        ]
        const expected = [[TokenType.BeginScope, undefined], ...expectedLiteral1,
            [TokenType.Text, "and"], ...expectedLiteral2, [TokenType.EndScope, undefined]]
    })

    it("Tokenize literal with invalid column index", () => {
        const literal = "[1, 4, $, 3]"
        expect(() => tokenize(literal))
            .toThrowError("SubspaceLogicTokenizer: Column indices of literals must be integers")
    })

    it("Tokenize literal with missing closing bracket", () => {
        const literal = "[1, 4, 3"
        expect(() => tokenize(literal))
            .toThrowError("SubspaceLogicTokenizer: Missing closing bracket ']'")
    })

})
