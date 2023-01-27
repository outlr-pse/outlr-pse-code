import {JSONSerializable} from "../JSONSerializable";
import {Subspace} from "./Subspace";
import {Outlier} from "./Outlier";

/**
 * This class represents an experiment result.
 */
export class ExperimentResult implements JSONSerializable {
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

    /**
     * This method returns the experiment result as a JSON object.
     * It is called by the JSON.stringify() method.
     */
    toJSON() {
        let outlierIndices = [];
        if (this.outliers != null) {
            for (let outlier of this.outliers) {
                outlierIndices.push(outlier.index);
            }
        }
        return {
            id: this.id,
            accuracy: this.accuracy,
            executionDate: this.executionDate,
            executionTime: this.executionTime,
            // subspaces: this.subspaces,
            // outliers: outlierIndices
        };
    }
    serialize(): string {
        return JSON.stringify(this);
    }

    /**
     * This method creates an experiment result from a JSON object.
     * @param jsonObject The JSON object.
     * @param subspaceMap The map of subspaces added to the experiment result.
     * @param outlierMap The map of outliers added to the experiment result.
     */
    static fromJSONObject(jsonObject: any, subspaceMap: Map<number, Subspace>, outlierMap: Map<number, Outlier>): ExperimentResult {
        return new ExperimentResult(
            jsonObject.id,
            jsonObject.accuracy,
            new Date(jsonObject.executionDate),
            jsonObject.executionTime,
            Array.from(subspaceMap.values()),
            Array.from(outlierMap.values()));
    }
}