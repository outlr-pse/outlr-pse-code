
export const enum TokenType {
  BeginLit, EndLit, BeginScope, EndScope, Text, Cols
}

export type Token = [TokenType, any?]

export function tokenize(expression: string): Token[] {
  let tokens: Token[] = []
  let i = 0
  while (i < expression.length) {
    const firstChar = expression.charAt(i)
    if (firstChar == '[') {
      i = tokenizeLiteral(expression, i + 1, tokens)
    } else if (firstChar == '(') {
      tokens.push([TokenType.BeginScope, undefined])
      i += 1
    } else if (firstChar == ')') {
      tokens.push([TokenType.EndScope, undefined])
      i += 1
    } else if (letterRegex.test(firstChar)) {
      i = tokenizeText(expression, i, tokens)
    } else if (whitespaceRegex.test(firstChar)) {
      // Ignore
      i += 1
    } else {
      throw new Error("SubspaceLogicTokenizer: Unexpected character: " + firstChar)
    }
  }
  return tokens
}

function tokenizeLiteral(expression: string, begin: number, tokens: Token[]): number {
  tokens.push([TokenType.BeginLit, undefined])
  let end = expression.indexOf(']', begin)
  if (end == -1) {
    throw new Error("SubspaceLogicTokenizer: Missing closing bracket ']'")
  }
  const split = expression.substring(begin, end)
    .split(',')
    .map(str => str.trim())
  if (split.length == 1 && !nonWhitespaceRegex.test(split[0]))
    throw new Error("SubspaceLogicTokenizer: Column indices of literals must not be empty")

  const cols = split.map(str => parseInt(str))
  if (cols.some(isNaN))
    throw new Error("SubspaceLogicTokenizer: Column indices of literals must be integers: " + cols)

  tokens.push([TokenType.Cols, cols])
  tokens.push([TokenType.EndLit, undefined])
  return end + 1
}

function tokenizeText(expression: string, begin: number, tokens: Token[]): number {
  let end = begin + 1
  while (end < expression.length && letterRegex.test(expression.charAt(end))) {
    end += 1
  }
  let word = expression.substring(begin, end)
  tokens.push([TokenType.Text, word])
  return end
}

const letterRegex = /[a-zA-Z]/
const whitespaceRegex = /\s/ // Matches space, tab, newline
const nonWhitespaceRegex = /\S/ // Matches anything except space, tab, newline
