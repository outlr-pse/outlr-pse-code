import { type SubspaceLogic } from '../../models/subspacelogic/SubspaceLogic'
import { Subspace } from '../../models/results/Subspace'
import { Literal } from '../../models/subspacelogic/Literal'
import { Operation } from '../../models/subspacelogic/Operation'

/**
 * Parse a simple version of the subspace logic syntax
 * The allowed syntax is [sub] op [sub] op ... [sub]
 * where sub can be a comma seperated listing of integers
 * and op can be either "and" or "or"
 * Semantically the logic is interpreted right associatively.
 * So for example [0] and [1] and [2] is interpreted as [0] and ([1] and [2]).
 * Note that parenthesis are currently not allowed
 * @param input Subspace logic syntax
 * @param startIndex The start index of the input. Default value is 0
 */
export function parseSubspaceLogic (input: string, startIndex: number = 0): SubspaceLogic | null {
  // console.log("Parsing subspace logic: " + input.substring(startIndex))
  const [subspace, restIndex] = readSubspace(input, startIndex)
  if (subspace === null) {
    return null
  }
  const restLogic = parseSubspaceLogic(input, restIndex)
  if (restLogic === null) {
    return new Literal(subspace)
  } else {
    const operatorStr: any = input.substring(restIndex, input.indexOf('[', restIndex)).trim()
    return new Operation(
      operatorStr,
      [new Literal(subspace), restLogic])
  }
}

function readSubspace (input: string, startIndex: number): [Subspace | null, number] {
  // console.log("Parsing subspace: " + input.substring(startIndex))
  const startSubspace = input.indexOf('[', startIndex)
  if (startSubspace == -1) { return [null, startIndex] }
  const endSubspace = input.indexOf(']', startIndex)
  const columns: number[] = input.substring(startSubspace + 1, endSubspace)
    .split(',')
    .map((str) => parseInt(str.trim()))
  return [new Subspace(null, null, columns), endSubspace + 1]
}
