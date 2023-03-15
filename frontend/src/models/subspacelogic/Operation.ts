import { type Operator } from './Operator'
import { SubspaceLogic } from './SubspaceLogic'
import { type Subspace } from '../results/Subspace'
import { type Outlier } from '../results/Outlier'

/**
 * This class represents an operation in the {@link SubspaceLogic}
 */
export class Operation implements SubspaceLogic {
  readonly operator: Operator
  readonly operands: SubspaceLogic[]

  /**
     * Create a new Operation
     * @param operator Operator
     * @param operands Operands (must contain at least one element)
     * @throws Throws if the `operands` parameter was empty
     */
  constructor (operator: Operator, operands: SubspaceLogic[]) {
    if (operands.length === 0) { throw new Error('Tried to create Operation with no operands') }
    this.operator = operator
    this.operands = operands
  }

  /**
     * Reads an Operation from a JSON object
     * Expects the jsonObject to a valid representation of an Operation
     * @param jsonObject JSON as an object. This is what {@link JSON.parse} returns
     * @param subspaceMap A map that maps subspace ids to {@link Subspace} objects.
     *      Will be modified. Also, the subspaces in the map will be modified.
     *      If an id exists in this map, the corresponding subspace is used in the subspace logic.
     *      Otherwise, a new subspace is created and also added to the map.
     *      So after the operation is created all subspaces that are used will be in the map
     * @param outlierMap A map that maps outlier ids to {@link Outlier} objects.
     *      Will be modified. Also, the outlier in the map will be modified.
     *      If an id exists in this map, the corresponding outlier object is used in the subspaces
     *      that are part of the subspace logic.
     *      Otherwise, a new outlier is created and added to the map.
     *      So after the operation is created all outliers that are used will be in the map.
     * @throws Throws when the given JSON object is not a valid SubspaceLogic
     */
  public static fromJSONObject (
    jsonObject: any,
    subspaceMap: Map<number, Subspace>,
    outlierMap: Map<number, Outlier>
  ): Operation {
    return new Operation(jsonObject.operator, jsonObject.operands.map(
      (subspaceLogicJson: any) => SubspaceLogic.fromJSONObject(subspaceLogicJson, subspaceMap, outlierMap))
    )
  }

  /**
     * Converts Operation to a json object
     */
  public toJSON () {
    return {
      operation: {
        operator: this.operator,
        operands: this.operands
      }
    }
  }

  serialize (): string {
    return JSON.stringify(this)
  }
}
