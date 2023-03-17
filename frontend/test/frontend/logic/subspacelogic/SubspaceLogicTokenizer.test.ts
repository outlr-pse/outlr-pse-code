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

  it("Tokenize literal without columns", () => {
    expect(() => tokenize("[]"))
      .toThrow("SubspaceLogicTokenizer: Column indices of literals must not be empty")
  })

  it("Tokenize literal with spaces and newlines", () => {
    const literal = "\n[ \n1  \n,   2  \n,  \n\n\n 3]\n"
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

    const actual = tokenize(operation)
    expect(actual).toEqual(expected)
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

    const actual = tokenize(operation)
    expect(actual).toEqual(expected)
  })

  it("Tokenize ternary operation", () => {
    const literal1 = "[1,2,3]"
    const literal2 = "[4,5,6]"
    const literal3 = "[7,8,9]"
    const operation = "(" + literal1 + " and " + literal2 + " and " + literal3 + ")"

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
    const expectedLiteral3 = [
      [TokenType.BeginLit, undefined],
      [TokenType.Cols, [7, 8, 9]],
      [TokenType.EndLit, undefined]
    ]
    const expected = [
      [TokenType.BeginScope, undefined], ...expectedLiteral1,
      [TokenType.Text, "and"], ...expectedLiteral2,
      [TokenType.Text, "and"], ...expectedLiteral3,
      [TokenType.EndScope, undefined]]

    const actual = tokenize(operation)
    expect(actual).toEqual(expected)
  })

  it("Tokenize nested ternary operation", () => {
    const literal1 = "[1,2,3]"
    const literal2 = "[4,5,6]"
    const literal3 = "[7,8,9]"
    const innerOperation1 = "(" + literal1 + " and " + literal2 + ")"
    const innerOperation2 = "(" + literal2 + " or " + literal3 + ")"
    const operation = "  (" + innerOperation1 + "or" + innerOperation2 + "or   " + literal1 + "  )  "

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
    const expectedLiteral3 = [
      [TokenType.BeginLit, undefined],
      [TokenType.Cols, [7, 8, 9]],
      [TokenType.EndLit, undefined]
    ]
    const expectedInnerOperation1 = [
      [TokenType.BeginScope, undefined], ...expectedLiteral1,
      [TokenType.Text, "and"], ...expectedLiteral2,
      [TokenType.EndScope, undefined]
    ]
    const expectedInnerOperation2 = [
      [TokenType.BeginScope, undefined], ...expectedLiteral2,
      [TokenType.Text, "or"], ...expectedLiteral3,
      [TokenType.EndScope, undefined]
    ]
    const expected = [
      [TokenType.BeginScope, undefined], ...expectedInnerOperation1,
      [TokenType.Text, "or"], ...expectedInnerOperation2,
      [TokenType.Text, "or"], ...expectedLiteral1,
      [TokenType.EndScope, undefined]
    ]

    const actual = tokenize(operation)
    expect(actual).toEqual(expected)
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
