import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";
import {ExperimentResult} from "../results/ExperimentResult";
import {ODM} from "../odm/ODM";

export class Experiment implements JSONSerializable, JSONDeserializable {
    id: number | null;
    name: string;
    datasetName: string | null;
    dataset: File | null;
    groundTruth: File | null;
    odm: ODM;
    subspaceLogic: string | null;//SubspaceLogic class
    experimentResult: ExperimentResult | null;

    constructor(name: string,
                datasetName: string | null,
                dataset: File | null,
                groundTruth: File | null,
                odm: ODM,
                subspaceLogic: string) {
        this.id = null;
        this.name = name;
        this.datasetName = datasetName;
        this.dataset = dataset;
        this.groundTruth = groundTruth;
        this.odm = odm;
        this.subspaceLogic = subspaceLogic;
        this.experimentResult = null;
    }

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

    public static fromJSON(json: string): Experiment {
        let experiment = new Experiment("", "", null, null, new ODM("", []), "");
        experiment.deserialize(json);
        return experiment;
    }

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