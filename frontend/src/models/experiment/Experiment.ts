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
    datasetName: string;
    dataset: File | null;
    groundTruth: File | null;
    odm: ODM;
    subspaceLogic: SubspaceLogic | null;
    experimentResult: ExperimentResult | null;
    running: boolean = false;

    constructor(name: string,
                datasetName: string,
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
        this.running = false;
    }

    /**
     * This method returns the experiment as a JSON object.
     * It is called by the JSON.stringify() method.
     */
    toJSON() {
        return {
            name: this.name,
            dataset: this.dataset,
            dataset_name: this.datasetName,
            ground_truth: this.groundTruth,
            odm: this.odm,
            subspace_logic: this.subspaceLogic,
        };

    }

    /**
     * This method creates an experiment from a JSON string.
     * @param json
     */
    public static fromJSON(json: string): Experiment {
        let experiment = new Experiment("", "", null, null, new ODM(0, "", []));
        experiment.deserialize(json);
        return experiment;
    }

    /**
     * This method deserializes the experiment from a JSON string.
     * When the experiment result is given, the experiment is not running anymore.
     * @param json The JSON string.
     */
    deserialize(json: string): void {
        let jsonObject = JSON.parse(json);
        this.id = jsonObject.id;
        this.name = jsonObject.name;
        this.datasetName = jsonObject.dataset_name;
        this.odm = ODM.fromJSON(jsonObject.odm, jsonObject.param_values);

        let subspaceMap = new Map<number, Subspace>();
        let outlierMap = new Map<number, Outlier>();

        if (jsonObject.subspace_logic != null) {
            this.subspaceLogic = SubspaceLogic.fromJSONObject(jsonObject.subspace_logic, subspaceMap, outlierMap);
        } else {
            this.subspaceLogic = null;
        }
        if (jsonObject.experiment_result != undefined) {
            this.experimentResult = ExperimentResult.fromJSONObject(jsonObject.experiment_result, subspaceMap, outlierMap);
            this.running = false;
        } else {
            this.running = true
        }

    }

    serialize(): string {
        return JSON.stringify(this);
    }


}