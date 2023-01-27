import {JSONSerializable} from "../JSONSerializable"
import {Operation} from "./Operation";
import {Literal} from "./Literal";
import {Subspace} from "../results/Subspace";
import {Outlier} from "../results/Outlier";

/**
 * This interface represents the subspace logic using a composite pattern
 */
export abstract class SubspaceLogic implements JSONSerializable {

    /**
     * Reads a SubspaceLogic from JSON
     * @param json JSON as a string
     * @throws Throws when the given JSON object is not a valid SubspaceLogic
     */
    public static fromJSON(json: string): SubspaceLogic {
        return SubspaceLogic.fromJSONObject(JSON.parse(json), new Map<number, Subspace>(), new Map<number, Outlier>)
    }

    /**
     * Reads a SubspaceLogic from a JSON object
     * @param jsonObject JSON as an object. This is what {@param subspaceMap
    @param outlierMap
    @link JSON.parse} returns
     * @throws Throws when the given JSON object is not a valid SubspaceLogic
     */
    public static fromJSONObject(jsonObject: any, subspaceMap: Map<number, Subspace>, outlierMap: Map<number, Outlier>): SubspaceLogic {
        // Find out the type of the logic's root and the call the corresponding fromJSONObject method
        const roots = Object.keys(jsonObject)
        if (roots.length > 1)
            throw new Error("Tries to read SubspaceLogic from JSON where a node had multiple keys")
        const root = roots[0]
        switch (root) {
            case "operation": return Operation.fromJSONObject(jsonObject.operation, subspaceMap, outlierMap);
            case "literal": return Literal.fromJSONObject(jsonObject.literal, subspaceMap, outlierMap);
            default:
                throw new Error(`Tried to read SubspaceLogic from JSON which had the unknown root element '${root}'`)
        }

    }

    public abstract serialize(): string
}
