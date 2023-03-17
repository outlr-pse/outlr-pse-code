import { type JSONSerializable } from '../JSONSerializable'
import { Operation } from './Operation'
import { Literal } from './Literal'
import { type Subspace } from '../results/Subspace'
import { type Outlier } from '../results/Outlier'

/**
 * This interface represents the subspace logic using a composite pattern
 */
export abstract class SubspaceLogic implements JSONSerializable {
  /**
     * Reads a SubspaceLogic from JSON
     * @param json JSON as a string
     * @throws Throws when the given JSON object is not a valid SubspaceLogic
     */
  public static fromJSON (json: string): SubspaceLogic {
    return SubspaceLogic.fromJSONObject(JSON.parse(json), new Map<number, Subspace>(), new Map<number, Outlier>())
  }

  /**
     * Reads a SubspaceLogic from a JSON object
     * @param jsonObject JSON as an object. This is what {@link JSON.parse} returns
     * @param subspaceMap A map that maps subspace ids to {@link Subspace} objects.
     *      Will be modified. Also, the subspaces in the map will be modified.
     *      If an id exists in this map, the corresponding subspace is used in the subspace logic.
     *      Otherwise, a new subspace is created and also added to the map.
     *      So after the subspace logic is created all subspaces that are used will be in the map
     * @param outlierMap A map that maps outlier ids to {@link Outlier} objects.
     *      Will be modified. Also, the outlier in the map will be modified.
     *      If an id exists in this map, the corresponding outlier object is used in the subspaces
     *      that are part of the subspace logic.
     *      Otherwise, a new outlier is created and added to the map.
     *      So after the subspace logic is created all outliers that are used will be in the map.
     * @throws Throws when the given JSON object is not a valid SubspaceLogic
     */
  public static fromJSONObject (
    jsonObject: any,
    subspaceMap: Map<number, Subspace>,
    outlierMap: Map<number, Outlier>
  ): SubspaceLogic {
    // Find out the type of the logic's root and the call the corresponding fromJSONObject method
    const roots = Object.keys(jsonObject)
    if (roots.length > 1) { throw new Error('Tries to read SubspaceLogic from JSON where a node had multiple keys') }
    const root = roots[0]
    switch (root) {
      case 'operation': return Operation.fromJSONObject(jsonObject.operation, subspaceMap, outlierMap)
      case 'literal': return Literal.fromJSONObject(jsonObject.literal, subspaceMap, outlierMap)
      default:
        throw new Error(`Tried to read SubspaceLogic from JSON which had the unknown root element '${root}'`)
    }
  }

  /**
   * Returns the expression represented by this subspace logic
   * The expression is not necessarily exactly the same as the one that was used to parse the subspace logic
   * @returns The expression represented by this subspace logic as a string
   */
  public abstract toExpression (): string

  public abstract serialize (): string
}
