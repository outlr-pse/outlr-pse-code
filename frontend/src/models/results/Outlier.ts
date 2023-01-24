import {Subspace} from "./Subspace";

export class Outlier {
    index: number;
    subspaces: Subspace[];

    constructor(index: number, subspaces: Subspace[]) {
        this.index = index;
        this.subspaces = subspaces;
    }


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