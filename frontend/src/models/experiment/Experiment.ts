import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";
import {ExperimentResult} from "../results/ExperimentResult";
import {ODM} from "../odm/ODM";
import {SubspaceLogic} from "../subspacelogic/SubspaceLogic";

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
                subspaceLogic: SubspaceLogic) {
        this.id = null;
        this.name = name;
        this.datasetName = datasetName;
        this.dataset = dataset;
        this.groundTruth = groundTruth;
        this.odm = odm;
        this.subspaceLogic = subspaceLogic;
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

    // /**
    //  * This method creates an experiment from a JSON string.
    //  * @param json
    //  */
    // public static fromJSON(json: string): Experiment {
    //     let experiment = new Experiment("", "", null, null, new ODM("", []), new SubspaceLogic(""));
    //     experiment.deserialize(json);
    //     return experiment;
    // }

    deserialize(json: string): void {
        let jsonObject = JSON.parse(json);
        this.id = jsonObject.id;
        this.name = jsonObject.name;
        this.datasetName = jsonObject.datasetName;
        this.dataset = jsonObject.dataset;
        this.groundTruth = jsonObject.groundTruth;
        this.odm = jsonObject.odm;
        this.subspaceLogic = jsonObject.subspaceLogic;
        this.experimentResult = jsonObject.experimentResult;

    }

    serialize(): string {
        return JSON.stringify(this);
    }


}