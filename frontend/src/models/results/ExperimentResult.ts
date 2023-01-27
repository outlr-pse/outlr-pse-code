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
    resultSpace: Subspace | undefined

    constructor(id: number,
                accuracy: number,
                executionDate: Date,
                executionTime: number,
                subspaces: Subspace[],
                outliers: Outlier[],
                resultSpace?: Subspace) {
        this.id = id;
        this.accuracy = accuracy;
        this.executionDate = executionDate;
        this.executionTime = executionTime;
        this.subspaces = subspaces;
        this.outliers = outliers;
        this.resultSpace = resultSpace;
    }

    /**
     * This method returns the experiment result as a JSON object.
     * It is called by the JSON.stringify() method.
     */
    toJSON() {
        return {
            id: this.id,
            accuracy: this.accuracy,
            executionDate: this.executionDate,
            executionTime: this.executionTime,
            resultSpace: this.resultSpace
        };
    }
    serialize(): string {
        return JSON.stringify(this);
    }

    /**
     * This method creates an experiment result from a JSON object.
     * @param jsonObject The JSON object.
     * @param subspaceMap The map of all subspaces that the experiment holds.
     * @param outlierMap The map of  all outliers that the experiment holds.
     */
    static fromJSONObject(jsonObject: any, subspaceMap: Map<number, Subspace>, outlierMap: Map<number, Outlier>): ExperimentResult {
        return new ExperimentResult(
            jsonObject.id,
            jsonObject.accuracy,
            new Date(jsonObject.executionDate),
            jsonObject.executionTime,
            Array.from(subspaceMap.values()),
            Array.from(outlierMap.values()),
            Subspace.fromJSONObject(jsonObject.resultSpace, outlierMap)
    );

    }
}