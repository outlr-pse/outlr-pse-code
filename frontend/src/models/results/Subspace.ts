import {Outlier} from "./Outlier";
import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";

/**
 * This class represents a subspace.
 */
export class Subspace implements JSONDeserializable, JSONSerializable {
    id: number | null;
    name: string | null;
    columns: number[];
    outliers: Outlier[] | null;
    rocCurve: Record<any, any>[] | null;

    constructor(id: number, name: string | null,
                columns: number[]) {
        this.id = id;
        this.name = name;
        this.columns = columns;
        this.outliers = null;
        this.rocCurve = null;

    }

    /**
     * This method returns the subspace as a JSON object.
     * It is called by the JSON.stringify() method.
     */
    toJSON() {
        return {
            id: this.id,
            name: this.name,
            columns: this.columns,
            outliers: this.outliers,
            rocCurve: this.rocCurve
        };
    }

    /**
     * This method creates a subspace from a JSON string.
     * @param json
     */
    public static fromJSON(json: string): Subspace {
        let subspace = new Subspace(0, null, []);
        subspace.deserialize(json);
        return subspace;
    }


    deserialize(json: string): void {
        let jsonObject = JSON.parse(json);
        this.name = jsonObject.name;
        this.columns = jsonObject.columns;
        this.rocCurve = jsonObject.rocCurve;
        let outlierArray = []
        for (let outlier of jsonObject.outliers){
            outlierArray.push(Outlier.fromJSON(outlier, [this]));
        }
        this.outliers = outlierArray;
    }

    serialize(): string {
        return JSON.stringify(this);
    }
}