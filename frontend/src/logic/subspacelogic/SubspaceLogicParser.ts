import type { SubspaceLogic } from '../../models/subspacelogic/SubspaceLogic'
import { type Token, tokenize, TokenType } from './SubspaceLogicTokenizer'
import { Subspace } from '../../models/results/Subspace'
import { Operator } from '../../models/subspacelogic/Operator'
import { Operation } from '../../models/subspacelogic/Operation'
import { Literal } from '../../models/subspacelogic/Literal'

/**
 * Parses a subspace logic expression
 * The expression must follow this grammar:
 *  Logic -> (Logic) | Literal | Logic Operator Logic Operator Logic ...
 *    where each Operator must be the same
 *  Operator -> and | or
 *  Literal -> [ comma separated list of integers ]
 * @throws Error if the expression cannot be tokenized or parsed
 */
export function parseSubspaceLogic (expression: string): SubspaceLogic {
  return parseSubspaceLogicTokens(tokenize(expression))
}

/**
 * Parses a subspace logic expression from a list of tokens
 * @param tokens Token list (see {@link tokenize})
 * @throws Error if the expression cannot be parsed
 */
export function parseSubspaceLogicTokens (tokens: Token[]): SubspaceLogic {
  const [logic] = parse(tokens, 0, false)
  // maybe check end here?
  return logic
}

/**
 * Parses a subspace logic expression from a list of tokens
 * @param tokens Token list
 * @param begin Index of the first token to parse
 * @param expectEndScope Whether the expression must end with an end scope token
 * @returns The parsed expression and the index of the first token after the expression
 * @throws Error if the expression cannot be parsed
 */
function parse (tokens: Token[], begin: number, expectEndScope: boolean): [SubspaceLogic, number] {
  let operator: Operator | null = null
  const operands: SubspaceLogic[] = []

  let current = begin
  while (true) {
    // Ensure that there are tokens left
    if (current >= tokens.length) {
      throw new Error('SubspaceLogicParser: Unexpected end of tokens')
    }
    if (tokens[current][0] === TokenType.EndScope) {
      throw new Error('SubspaceLogicParser: Unexpected end of scope')
    }

    // Read operand
    const [operandType] = tokens[current]
    current += 1
    if (operandType === TokenType.BeginScope) {
      const [operand, end] = parse(tokens, current, true)
      operands.push(operand)
      current = end
    } else if (operandType === TokenType.BeginLit) {
      const [literal, end] = parseLiteral(tokens, current)
      operands.push(literal)
      current = end
    } else {
      throw new Error(`SubspaceLogicParser: Unexpected token type for operand: ${operandType}`)
    }

    // Check if end is reached
    if (current >= tokens.length) {
      if (expectEndScope) throw new Error('SubspaceLogicParser: Missing end of scope')
      break
    } else if (tokens[current][0] === TokenType.EndScope) {
      if (!expectEndScope) throw new Error('SubspaceLogicParser: Unexpected end of scope')
      current += 1
      break
    }

    // If not end, read operator
    const [operatorToken, operatorValue] = tokens[current]
    current += 1
    if (operatorToken !== TokenType.Text) {
      throw new Error(`SubspaceLogicParser: Expected operator, got ${operatorToken}`)
    }
    const readOperator = parseOperator(operatorValue)
    if (operator === null) { // First time reading operator
      operator = readOperator
    } else if (operator !== readOperator) { // Operator different from previously read
      throw new Error('SubspaceLogicParser: Found different operators in one scope')
    }
  }

  if (operands.length === 1) {
    return [operands[0], current]
  }
  if (operator === null) {
    throw new Error('SubspaceLogicParser: Impossible state: operator is null')
  }
  return [new Operation(operator, operands), current] // operator is not null here
}

/**
 * Parses a literal from a list of tokens
 * @param tokens Token list
 * @param begin Index of the first token to parse
 * @returns The parsed literal and the index of the first token after the literal
 * @throws Error if the literal cannot be parsed
 */
function parseLiteral (tokens: Token[], begin: number): [Literal, number] {
  const [tokenType, tokenValue] = tokens[begin]
  if (tokenType !== TokenType.Cols) {
    throw new Error(`SubspaceLogicParser: Expected subspace columns, got ${tokenType}`)
  }
  if (tokens[begin + 1][0] !== TokenType.EndLit) {
    throw new Error(`SubspaceLogicParser: Expected end of literal, got ${tokens[begin + 1][0]}`)
  }

  // tokenValue is the list of column indices
  return [new Literal(newSubspace(tokenValue)), begin + 2] // 2 tokens were consumed
}

/**
 * Parses an operator from a string
 * @param operator Operator as string
 * @returns The parsed operator (see {@link Operator})
 * @throws Error if the operator is unknown
 */
function parseOperator (operator: string): Operator {
  switch (operator) {
    case 'and': return Operator.AND
    case 'or': return Operator.OR
    default: throw new Error(`SubspaceLogicParser: Unknown operator: ${operator}`)
  }
}

function newSubspace (cols: number[]): Subspace {
  return new Subspace(null, null, cols)
}
