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




}