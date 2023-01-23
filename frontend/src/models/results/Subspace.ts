import {Outlier} from "./Outlier";
import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";

export class Subspace implements JSONDeserializable, JSONSerializable {
    name: string | null;
    columns: number[];
    outliers: Outlier[] | null;
    rocCurve: Record<any, any>[] | null;

    constructor(name: string | null,
                columns: number[]) {
        this.name = name;
        this.columns = columns;
        this.outliers = null;
        this.rocCurve = null;

    }

    toJSON() {
        return {
            name: this.name,
            columns: this.columns,
            outliers: this.outliers,
            rocCurve: this.rocCurve
        };
    }

    public static fromJSON(json: string): Subspace {
        let subspace = new Subspace(null, []);
        subspace.deserialize(json);
        return subspace;
    }


    deserialize(json: string): void {
        let jsonObject = JSON.parse(json);
        this.name = jsonObject.name;
        this.columns = jsonObject.columns;
        this.outliers = jsonObject.outliers;
        this.rocCurve = jsonObject.rocCurve;
    }

    serialize(): string {
        return JSON.stringify(this);
    }
}