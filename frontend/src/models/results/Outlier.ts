import {Subspace} from "./Subspace";

export class Outlier {
    index: number;
    subspaces: Subspace[];

    constructor(index: number, subspaces: Subspace[]) {
        this.index = index;
        this.subspaces = subspaces;
    }
}