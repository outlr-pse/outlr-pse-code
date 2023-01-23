import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";
import {Subspace} from "./Subspace";
import {Outlier} from "./Outlier";

export class ExperimentResult implements JSONDeserializable, JSONSerializable {
    id: number;
    accuracy: number;
    executionDate: Date;
    executionTime: number;
    subspaces: Subspace[];
    outliers: Outlier[];

    constructor(id: number,
                accuracy: number,
                executionDate: Date,
                executionTime: number,
                subspaces: Subspace[],
                outliers: Outlier[]) {
        this.id = id;
        this.accuracy = accuracy;
        this.executionDate = executionDate;
        this.executionTime = executionTime;
        this.subspaces = subspaces;
        this.outliers = outliers;
    }
    toJSON() {
        return {
            id: this.id,
            accuracy: this.accuracy,
            executionDate: this.executionDate,
            executionTime: this.executionTime,
            subspaces: this.subspaces,
            outliers: this.outliers
        };
    }
    public static fromJSON(json: string): ExperimentResult {
        let experimentResult = new ExperimentResult(0, 0, new Date(), 0, [], []);
        experimentResult.deserialize(json);
        return experimentResult;
    }

    deserialize(json: string): void {
        let jsonObject = JSON.parse(json);
        this.id = jsonObject.id;
        this.accuracy = jsonObject.accuracy;
        this.executionDate = jsonObject.executionDate;
        this.executionTime = jsonObject.executionTime;
        this.subspaces = jsonObject.subspaces;
        this.outliers = jsonObject.outliers;
    }

    serialize(): string {
        return JSON.stringify(this);
    }

}