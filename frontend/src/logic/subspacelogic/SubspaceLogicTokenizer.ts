
export const enum TokenType {
  /** Begin of a literal */
  BeginLit,

  /** End of a literal */
  EndLit,

  /** Begin of a scope */
  BeginScope,

  /** End of a scope */
  EndScope,

  /** text (used for operators), value is a string */
  Text,

  /** Comma seperated list of column indices, value is an int list */
  Cols
}

/** A token consists of a type and an optional value. */
export type Token = [TokenType, any?]

/**
 * Converts an expression into a list of tokens, that represent the expression.
 * @throws Error if the expression cannot be tokenized
 */
export function tokenize (expression: string): Token[] {
  const tokens: Token[] = []
  let i = 0
  while (i < expression.length) {
    const firstChar = expression.charAt(i)
    if (firstChar === '[') {
      i = tokenizeLiteral(expression, i + 1, tokens)
    } else if (firstChar === '(') {
      tokens.push([TokenType.BeginScope, undefined])
      i += 1
    } else if (firstChar === ')') {
      tokens.push([TokenType.EndScope, undefined])
      i += 1
    } else if (letterRegex.test(firstChar)) {
      i = tokenizeText(expression, i, tokens)
    } else if (whitespaceRegex.test(firstChar)) {
      // Ignore
      i += 1
    } else {
      throw new Error('SubspaceLogicTokenizer: Unexpected character: ' + firstChar)
    }
  }
  return tokens
}

/**
 * Tokenizes an expression that describes a literal
 * @param expression Expression that describes a literal
 * @param begin Index of the first character of the literal (does not include the opening bracket)
 * @param tokens Token list to append the tokens to
 * @returns Index of the first character after the closing bracket of the literal
 */
function tokenizeLiteral (expression: string, begin: number, tokens: Token[]): number {
  tokens.push([TokenType.BeginLit, undefined])
  const end = expression.indexOf(']', begin)
  if (end === -1) {
    throw new Error('SubspaceLogicTokenizer: Missing closing bracket \']\'')
  }
  const split = expression.substring(begin, end)
    .split(',')
    .map(str => str.trim())
  if (split.length === 1 && !nonWhitespaceRegex.test(split[0])) { throw new Error('SubspaceLogicTokenizer: Column indices of literals must not be empty') }

  const cols = split.map(str => parseInt(str))
  if (cols.some(isNaN)) { throw new Error('SubspaceLogicTokenizer: Column indices of literals must be integers') }

  tokens.push([TokenType.Cols, cols])
  tokens.push([TokenType.EndLit, undefined])
  return end + 1
}

/**
 * Tokenizes a text token
 * @param expression Text expression
 * @param begin Index of the first character of the text
 * @param tokens Token list to append the tokens to
 * @returns Index of the first character after the text
 */
function tokenizeText (expression: string, begin: number, tokens: Token[]): number {
  let end = begin + 1
  while (end < expression.length && letterRegex.test(expression.charAt(end))) {
    end += 1
  }
  const word = expression.substring(begin, end)
  tokens.push([TokenType.Text, word])
  return end
}

const letterRegex = /[a-zA-Z]/
const whitespaceRegex = /\s/ // Matches space, tab, newline
const nonWhitespaceRegex = /\S/ // Matches anything except space, tab, newline
