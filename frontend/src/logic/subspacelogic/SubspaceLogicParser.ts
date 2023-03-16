import {SubspaceLogic} from "../../models/subspacelogic/SubspaceLogic";
import {Token, TokenType} from "./SubspaceLogicTokenizer";
import {Subspace} from "../../models/results/Subspace";
import {Operator} from "../../models/subspacelogic/Operator";
import {Operation} from "../../models/subspacelogic/Operation";
import {Literal} from "../../models/subspacelogic/Literal";

export function parseSubspaceLogic(tokens: Token[]): SubspaceLogic {
    const [logic, _] = parse(tokens, 0, false)
    // maybe check end here?
    return logic
}

function parse(tokens: Token[], begin: number, expectEndScope: boolean): [SubspaceLogic, number] {
    let operator: Operator | null = null
    let operands: SubspaceLogic[] = []

    let current = begin
    while(true) {

        // Ensure that there are tokens left
        if (current >= tokens.length)
            throw new Error("SubspaceLogicParser: Unexpected end of tokens")
        if (tokens[current][0] == TokenType.EndScope)
            throw new Error("SubspaceLogicParser: Unexpected end of scope")

        // Read operand
        let [operandType, _] = tokens[current]
        current += 1
        if (operandType == TokenType.BeginScope) {
            let [operand, end] = parse(tokens, current, true)
            operands.push(operand)
            current = end
        }
        else if (operandType == TokenType.BeginLit) {
            let [literal, end] = parseLiteral(tokens, current)
            operands.push(literal)
            current = end
        }
        else {
            throw new Error("SubspaceLogicParser: Unexpected token type for operand: " + operandType)
        }

        // Check if end is reached
        if (current >= tokens.length) {
            if (expectEndScope) throw new Error("SubspaceLogicParser: Missing end of scope")
            break
        }
        else if (tokens[current][0] == TokenType.EndScope) {
            if (!expectEndScope) throw new Error("SubspaceLogicParser: Unexpected end of scope")
            current += 1
            break
        }

        // If not end, read operator
        let [operatorToken, operatorValue] = tokens[current]
        current += 1
        if (operatorToken != TokenType.Text)
            throw new Error("SubspaceLogicParser: Expected operator, got " + operatorToken)
        const readOperator = parseOperator(operatorValue)
        if (operator == null) // First time reading operator
            operator = readOperator
        else if (operator != readOperator) // Operator different from previously read
            throw new Error("SubspaceLogicParser: Found different operators in one scope")
    }
    if (operands.length == 1)
        return [operands[0], current]
    return [new Operation(operator!, operands), current] // operator is not null here
}

function parseLiteral(tokens: Token[], begin: number): [SubspaceLogic, number] {
    let [tokenType, tokenValue] = tokens[begin]
    if (tokenType != TokenType.Cols)
        throw new Error("SubspaceLogicParser: Expected subspace columns, got " + tokenType)
    if (tokens[begin + 1][0] != TokenType.EndLit)
        throw new Error("SubspaceLogicParser: Expected end of literal, got " + tokens[begin + 1][0])

    // tokenValue is the list of column indices
    return [new Literal(newSubspace(tokenValue)), begin + 2] // 2 tokens were consumed
}

function parseOperator(operator: string): Operator {
    switch (operator) {
        case "and": return Operator.AND
        case "or": return Operator.OR
        default: throw new Error("SubspaceLogicParser: Unknown operator: " + operator)
    }
}

function newSubspace(cols: number[]): Subspace {
    return new Subspace(null, null, cols)
}
