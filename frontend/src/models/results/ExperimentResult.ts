import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";
import {Subspace} from "./Subspace";
import {Outlier} from "./Outlier";

/**
 * This class represents an experiment result.
 */
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

    /**
     * This method returns the experiment result as a JSON object.
     * It is called by the JSON.stringify() method.
     */
    toJSON() {
        let outlierIndices = [];
        if(this.outliers != null){
            for(let outlier of this.outliers){
                outlierIndices.push(outlier.index);
            }
        }

        return {
            id: this.id,
            accuracy: this.accuracy,
            executionDate: this.executionDate,
            executionTime: this.executionTime,
            subspaces: this.subspaces,
            outliers: outlierIndices
        };
    }

    /**
     * This method creates an experiment result from a JSON string.
     * @param json
     */
    public static fromJSON(json: string): ExperimentResult {
        let experimentResult = new ExperimentResult(0, 0, new Date(), 0, [], []);
        experimentResult.deserialize(json);
        return experimentResult;
    }

    deserialize(json: string): void {
        let OutlierMap = new Map<number, Outlier>();
        let jsonObject = JSON.parse(json);
        for (let outlier of jsonObject.outliers){
            OutlierMap.set(outlier, new Outlier(outlier, []))
        }
        this.id = jsonObject.id;
        this.accuracy = jsonObject.accuracy;
        this.executionDate = new Date(jsonObject.executionDate);
        this.executionTime = jsonObject.executionTime;
        for (let subspace of jsonObject.subspaces){
            let outlierIndices = subspace.outliers;
            subspace.outliers = [];
            for (let outlierIndex of outlierIndices){
                let outlier = OutlierMap.get(outlierIndex);
                outlier?.subspaces.push(subspace);
                subspace.outliers.push(outlier);
            }
        }
        this.subspaces =   jsonObject.subspaces;

        this.outliers = Array.from(OutlierMap.values());
    }

    serialize(): string {
        return JSON.stringify(this);
    }

}