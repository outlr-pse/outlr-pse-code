import {Operator} from "./Operator"
import {SubspaceLogic} from "./SubspaceLogic";

/**
 * This class represents an operation in the {@link SubspaceLogic}
 */
export class Operation implements SubspaceLogic {

    private readonly operator: Operator
    private readonly operands: SubspaceLogic[]

    /**
     * Create a new Operation
     * @param operator Operator
     * @param operands Operands (must contain at least one element)
     * @throws Throws if the `operands` parameter was empty
     */
    constructor(operator: Operator, operands: SubspaceLogic[]) {
        if (operands.length === 0)
            throw new Error("Tried to create Operation with no operands")
        this.operator = operator
        this.operands = operands
    }

    /**
     * Reads an Operation from a JSON object
     * Expects the jsonObject to a valid representation of an Operation
     * @param jsonObject JSON as an object. This is what {@link JSON.parse} returns
     * @throws Throws when the given JSON object is not a valid SubspaceLogic
     */
    public static fromJSONObject(jsonObject: any): Operation {
        return new Operation(jsonObject.operator, jsonObject.operands.map(SubspaceLogic.fromJSONObject))
    }

    /**
     * Converts Operation to a json object
     */
    public toJSON() {
        return {
            operation: {
                operator: this.operator,
                operands: this.operands
            }
        }
    }

    serialize(): string {
        return JSON.stringify(this);
    }



}
