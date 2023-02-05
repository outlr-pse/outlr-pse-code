import {Hyperparameter} from "./Hyperparameter";
import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";

/**
 * This class represents an ODM.
 */
export class ODM implements JSONSerializable, JSONDeserializable {
    id: number
    name: string;
    hyperParameters: Hyperparameter[];

    constructor(id: number, name: string, hyperParameters: Hyperparameter[]) {
        this.id = id;
        this.name = name;
        this.hyperParameters = hyperParameters;
    }

    /**
     * This method returns the ODM as a JSON object.
     * It is called by the JSON.stringify() method.
     */
    toJSON() {
        let hyperParametersJSON: { [key: number]: string } = {};
        for (let param of this.hyperParameters) {
            hyperParametersJSON[param.id] = param.value;
        }
        return {
            id: this.id,
            hyper_parameters: hyperParametersJSON
        };
    }

    public static fromJsonCreateExp(json: any): ODM {
        let odm = new ODM(0, "", []);
        odm.deserialize(json);
        return odm;
    }

    deserialize(json: any): void {
        this.id = json.id;
        this.name = json.name;
    }


    /**
     * This method creates an ODM from a JSON string.
     * @param json
     */
    public static fromJSON(json: any, valuesJson: any): ODM {
        let odm = new ODM(0, "", []);
        odm.deserializeODM(json, valuesJson);
        return odm;
    }

    deserializeODM(json: any, valuesJson: any): void {
        this.name = json.name;
        for (let param of json.hyper_parameters) {
            this.hyperParameters?.push(Hyperparameter.fromJSON(param, valuesJson));
        }
    }

    serialize(): string {
        return JSON.stringify(this);
    }
}