import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";
import {ExperimentResult} from "../results/ExperimentResult";
import {ODM} from "../odm/ODM";
import {SubspaceLogic} from "../subspacelogic/SubspaceLogic";
import {Subspace} from "../results/Subspace";
import {Outlier} from "../results/Outlier";

/**
 * This class represents an experiment.
 */
export class Experiment implements JSONSerializable, JSONDeserializable {
    id: number | null;
    name: string;
    datasetName: string | null;
    dataset: File | null;
    groundTruth: File | null;
    odm: ODM;
    subspaceLogic: SubspaceLogic | null;
    experimentResult: ExperimentResult | null;

    constructor(name: string,
                datasetName: string | null,
                dataset: File | null,
                groundTruth: File | null,
                odm: ODM,
                subspaceLogic?: SubspaceLogic) {
        this.id = null;
        this.name = name;
        this.datasetName = datasetName;
        this.dataset = dataset;
        this.groundTruth = groundTruth;
        this.odm = odm;
        this.subspaceLogic = subspaceLogic != undefined ? subspaceLogic : null;
        this.experimentResult = null;
    }

    /**
     * This method returns the experiment as a JSON object.
     * It is called by the JSON.stringify() method.
     */
    toJSON() {
        return {
            id: this.id,
            name: this.name,
            datasetName: this.datasetName,
            dataset: this.dataset,
            groundTruth: this.groundTruth,
            odm: this.odm,
            subspaceLogic: this.subspaceLogic,
            experimentResult: this.experimentResult
        };

    }

     /**
      * This method creates an experiment from a JSON string.
      * @param json
      */
     public static fromJSON(json: string): Experiment {
         let experiment = new Experiment("", "", null, null, new ODM("", []));
         experiment.deserialize(json);
         return experiment;
     }

    deserialize(json: string): void {
        let jsonObject = JSON.parse(json);
        this.id = jsonObject.id;
        this.name = jsonObject.name;
        this.datasetName = jsonObject.datasetName;
        this.odm = jsonObject.odm;

        let subspaceMap = new Map<number, Subspace>();
        let outlierMap = new Map<number, Outlier>();

        this.subspaceLogic = SubspaceLogic.fromJSONObject(jsonObject.subspaceLogic, subspaceMap, outlierMap);
        this.experimentResult = ExperimentResult.fromJSONObject(jsonObject.experimentResult, subspaceMap, outlierMap);

    }

    serialize(): string {
        return JSON.stringify(this);
    }


}