import {parseSubspaceLogic, parseSubspaceLogicTokens} from "../../../../src/logic/subspacelogic/SubspaceLogicParser"
import {TokenType, Token} from "../../../../src/logic/subspacelogic/SubspaceLogicTokenizer"
import {Operation} from "../../../../src/models/subspacelogic/Operation"
import {Literal} from "../../../../src/models/subspacelogic/Literal"
import {Subspace} from "../../../../src/models/results/Subspace";
import {Operator} from "../../../../src/models/subspacelogic/Operator";


function makeLiteral(cols: number[]): Literal {
    return new Literal(new Subspace(null, null, cols))
}

function wrapInScope(tokens: Token[]): Token[] {
    return [[TokenType.BeginScope, undefined], ...tokens, [TokenType.EndScope, undefined]]
}

function unwrapFromScope(tokens: Token[]): Token[] {
    if (tokens[0][0] != TokenType.BeginScope || tokens[tokens.length - 1][0] != TokenType.EndScope)
        throw new Error("SubspaceLogicParser Test case is broken: Cannot construct token array correctly for testing")
    return tokens.slice(1, tokens.length - 1)
}

const literal1: Token[] = [[TokenType.BeginLit, undefined], [TokenType.Cols, [1, 2, 3]], [TokenType.EndLit, undefined]]
const literal2: Token[] = [[TokenType.BeginLit, undefined], [TokenType.Cols, [4, 5, 6]], [TokenType.EndLit, undefined]]
const literal3: Token[] = [[TokenType.BeginLit, undefined], [TokenType.Cols, [7, 8, 9]], [TokenType.EndLit, undefined]]

const binaryOperation: Token[] = wrapInScope([
    ...literal1,
    [TokenType.Text, "and"],
    ...literal2
])

const ternaryOperation: Token[] = wrapInScope([
    ...literal1,
    [TokenType.Text, "and"],
    ...literal2,
    [TokenType.Text, "and"],
    ...literal3
])

const nestedTernaryOperation: Token[] = wrapInScope([
    ...literal1,
    [TokenType.Text, "and"],
    ...binaryOperation,
    [TokenType.Text, "and"],
    ...literal3
])


const literal1Expected = makeLiteral([1, 2, 3])
const literal2Expected = makeLiteral([4, 5, 6])
const literal3Expected = makeLiteral([7, 8, 9])
const binaryOperationExpected = new Operation(Operator.AND, [literal1Expected, literal2Expected])
const ternaryOperationExpected = new Operation(Operator.AND, [literal1Expected, literal2Expected, literal3Expected])
const nestedTernaryOperationExpected = new Operation(Operator.AND, [literal1Expected, binaryOperationExpected, literal3Expected])

describe("SubspaceLogicParser", () => {

    it("Tokenize and parse binary operation", () => {
        const actual = parseSubspaceLogic("[1,2,3] and [4,5,6]")
        expect(actual).toEqual(binaryOperationExpected)
    })

    it("Tokenize and parse ternary operation in parenthesis", () => {
        const actual = parseSubspaceLogic("([1,2,3] and [4,5,6] and [7,8,9])")
        expect(actual).toEqual(ternaryOperationExpected)
    })

    it("Parse literal", () => {
        const actual = parseSubspaceLogicTokens(literal1)
        expect(actual).toEqual(literal1Expected)
    })

    it("Parse binary operation with and", () => {
        const actual = parseSubspaceLogicTokens(binaryOperation)
        const actualUnwrapped = parseSubspaceLogicTokens(unwrapFromScope(binaryOperation))
        expect(actual).toEqual(binaryOperationExpected)
        expect(actualUnwrapped).toEqual(binaryOperationExpected)
    })

    it("Parse binary operation with or", () => {
        const operation: Token[] = wrapInScope([
            ...literal1,
            [TokenType.Text, "or"],
            ...literal3
        ])
        const expected = new Operation(Operator.OR, [makeLiteral([1, 2, 3]), makeLiteral([7, 8, 9])])
        const actual = parseSubspaceLogicTokens(operation)
        const actualUnwrapped = parseSubspaceLogicTokens(unwrapFromScope(operation))
        expect(actual).toEqual(expected)
        expect(actualUnwrapped).toEqual(expected)
    })

    it("Parse ternary operation", () => {
        const actual = parseSubspaceLogicTokens(ternaryOperation)
        const actualUnwrapped = parseSubspaceLogicTokens(unwrapFromScope(ternaryOperation))
        expect(actual).toEqual(ternaryOperationExpected)
        expect(actualUnwrapped).toEqual(ternaryOperationExpected)
    })

    it("Parse nested operation", () => {
        const actual = parseSubspaceLogicTokens(nestedTernaryOperation)
        const actualUnwrapped = parseSubspaceLogicTokens(unwrapFromScope(nestedTernaryOperation))
        expect(actual).toEqual(nestedTernaryOperationExpected)
        expect(actualUnwrapped).toEqual(nestedTernaryOperationExpected)
    })

    it("Parse empty operation", () => {
        expect(() => parseSubspaceLogicTokens(wrapInScope([])))
            .toThrow("SubspaceLogicParser: Unexpected end of scope")
        expect(() => parseSubspaceLogicTokens([]))
            .toThrow("SubspaceLogicParser: Unexpected end of tokens")
    })

    it("Parse invalid operations", () => {
        const startWithEndScope: Token[] = [[TokenType.EndScope, undefined], ...literal1]
        const startWithEndLit: Token[] = [[TokenType.EndLit, undefined], ...literal1]
        const startWithText: Token[] = [[TokenType.Text, "and"], ...literal1]
        const startWithCols: Token[] = [[TokenType.Cols, [1, 2, 3]], ...literal1]
        const endWithBeginScope: Token[] = [...literal1, [TokenType.BeginScope, undefined]]
        const endWithBeginLit: Token[] = [...literal1, [TokenType.BeginLit, undefined]]
        const endWithText: Token[] = [...literal1, [TokenType.Text, "and"]]
        const endWithCols: Token[] = [...literal1, [TokenType.Cols, [1, 2, 3]]]

        expect(() => parseSubspaceLogicTokens(startWithEndScope))
            .toThrow("SubspaceLogicParser: Unexpected end of scope")
        expect(() => parseSubspaceLogicTokens(startWithEndLit))
            .toThrow("SubspaceLogicParser: Unexpected token type for operand: " + TokenType.EndLit)
        expect(() => parseSubspaceLogicTokens(startWithText))
            .toThrow("SubspaceLogicParser: Unexpected token type for operand: " + TokenType.Text)
        expect(() => parseSubspaceLogicTokens(startWithCols))
            .toThrow("SubspaceLogicParser: Unexpected token type for operand: " + TokenType.Cols)
        expect(() => parseSubspaceLogicTokens(endWithBeginScope))
            .toThrow("SubspaceLogicParser: Expected operator, got " + TokenType.BeginScope)
        expect(() => parseSubspaceLogicTokens(endWithBeginLit))
            .toThrow("SubspaceLogicParser: Expected operator, got " + TokenType.BeginLit)
        expect(() => parseSubspaceLogicTokens(endWithText))
            .toThrow("SubspaceLogicParser: Unexpected end of tokens")
        expect(() => parseSubspaceLogicTokens(endWithCols))
            .toThrow("SubspaceLogicParser: Expected operator, got " + TokenType.Cols)
    })

    it("Parse (a or b) and (c or d)", () => {
        const operation: Token[] = [
            [TokenType.BeginScope, undefined], ...literal3, [TokenType.Text, "or"], ...literal2, [TokenType.EndScope, undefined],
            [TokenType.Text, "and"],
            [TokenType.BeginScope, undefined], ...literal1, [TokenType.Text, "or"], ...literal2, [TokenType.EndScope, undefined]
        ]
        const expected = new Operation(Operator.AND, [
            new Operation(Operator.OR, [makeLiteral([7, 8, 9]), makeLiteral([4, 5, 6])]),
            new Operation(Operator.OR, [makeLiteral([1, 2, 3]), makeLiteral([4, 5, 6])])
        ])
        const actual = parseSubspaceLogicTokens(operation)
        const actualWrapped = parseSubspaceLogicTokens(wrapInScope(operation))
        expect(actual).toEqual(expected)
        expect(actualWrapped).toEqual(expected)
    })

})
