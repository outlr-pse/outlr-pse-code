import {Subspace} from "./Subspace";

/**
 * This class represents an outlier.
 */
export class Outlier {
    index: number;
    subspaces: Subspace[];

    constructor(index: number, subspaces: Subspace[]) {
        this.index = index;
        this.subspaces = subspaces;
    }

    /**
     * This method returns the outlier as a JSON object.
     * It is called by the JSON.stringify() method.
     */
    toJSON() {
        let subspaceIds = [];
        for (let subspace of this.subspaces){
            subspaceIds.push(subspace.id);
        }
        return {
            index: this.index,
            subspaces: subspaceIds
        };
    }

    /**
     * This method creates an outlier from a JSON string.
     * @param json
     * @param subspaces
     */
    public static fromJSON(json: string, subspaces: Subspace[]): Outlier {
        let outlier = new Outlier(0, []);
        outlier.deserialize(json, subspaces);
        return outlier;
    }

    deserialize(json: string, subspaces: Subspace[]): void {
        let jsonObject = JSON.parse(json);
        this.index = jsonObject.index;
        for (let subspace of subspaces) {
            if (jsonObject.subspaces.includes(subspace.id)) {
                this.subspaces.push(subspace);
            }
        }
    }


}