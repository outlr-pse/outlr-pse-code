import { Subspace } from '../results/Subspace'
import { type SubspaceLogic } from './SubspaceLogic'
import { type Outlier } from '../results/Outlier'

/**
 * This class represents a literal in the {@link SubspaceLogic}
 */
export class Literal implements SubspaceLogic {
  readonly subspace: Subspace

  /**
     * Create a new Literal
     * @param subspace Subspace
     */
  constructor (subspace: Subspace) {
    this.subspace = subspace
  }

  /**
     * Reads a Literal from a JSON object
     * Expects the jsonObject to a valid representation of a Literal
     * @param jsonObject JSON as an object. This is what {@link JSON.parse} returns
     * @param subspaceMap A map that maps subspace ids to {@link Subspace} objects.
     *      Will be modified. Also, the subspaces in the map will be modified.
     *      If the id of the literal's subspace exists in this map,
     *      the corresponding subspace is used for this literal.
     *      Otherwise, a new subspace is created and also added to the map.
     *      So after the literal is created its subspace will be in the map
     * @param outlierMap A map that maps outlier ids to {@link Outlier} objects.
     *      Will be modified. Also, the outlier in the map will be modified.
     *      If an id exists in this map, the corresponding outlier object is used in the literal's subspace.
     *      Otherwise, a new outlier is created and added to the map.
     *      So after the subspace logic is created all outliers that are used will be in the map.
     * @throws Throws when the given JSON object is not a valid SubspaceLogic
     */
  public static fromJSONObject (
    jsonObject: any,
    subspaceMap: Map<number, Subspace>,
    outlierMap: Map<number, Outlier>
  ): Literal {
    if (subspaceMap.has(jsonObject.subspace.id)) {
      return new Literal(subspaceMap.get(jsonObject.subspace.id) as Subspace)
    }
    const subspace = Subspace.fromJSONObject(jsonObject.subspace, outlierMap)
    subspaceMap.set(subspace.id as number, subspace)
    return new Literal(subspace)
  }

  /**
     * Converts Literal to a json object
     */
  public toJSON (): any {
    return { literal: { subspace: this.subspace } }
    // Possible issue: If a subspace appears multiple times in the subspace logic (which might be the case)
    // every appearance of the subspace is in the json completely.
    // The JSON could get very big potentially, because the subspace json can also contain an ROC curve
  }

  public serialize (): string {
    return JSON.stringify(this)
  }
}
