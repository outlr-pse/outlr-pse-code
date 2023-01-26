import {Subspace} from "../results/Subspace"
import {SubspaceLogic} from "./SubspaceLogic";

/**
 * This class represents a literal in the {@link SubspaceLogic}
 */
export class Literal implements SubspaceLogic {

    private readonly subspace: Subspace

    /**
     * Create a new Literal
     * @param subspace Subspace
     */
    constructor(subspace: Subspace) {
        this.subspace = subspace
    }

    /**
     * Reads a Literal from a JSON object
     * Expects the jsonObject to a valid representation of a Literal
     * @param jsonObject JSON as an object. This is what {@link JSON.parse} returns
     * @throws Throws when the given JSON object is not a valid SubspaceLogic
     */
    public static fromJSONObject(jsonObject: any): Literal {
        return new Literal(jsonObject.subspace)
    }

    /**
     * Converts Literal to a json object
     */
    public toJSON() {
        return { literal: { subspace: this.subspace } }
    }

    public serialize(): string {
        return JSON.stringify(this)
    }



}
