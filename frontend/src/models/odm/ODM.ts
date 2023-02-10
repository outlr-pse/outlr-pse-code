import {Hyperparameter} from "./Hyperparameter";
import {JSONSerializable} from "../JSONSerializable";

/**
 * This class represents an ODM.
 */
export class ODM implements JSONSerializable {
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
        let hyperParametersJSON: { [name: string]: string } = {};
        for (let param of this.hyperParameters) {
            if(param.value !== "") {
                hyperParametersJSON[param.name] = param.value;
            }
        }
        return {
            id: this.id,
            hyper_parameters: hyperParametersJSON
        };
    }

    /**
     * This method creates an ODM from a JSON string.
     * @param json The JSON string.
     * @param valuesJson The JSON string containing the hyperparameter values.
     */
    public static fromJSON(json: any, valuesJson?: any): ODM {
        let odm = new ODM(0, "", []);
        if (valuesJson) {
            odm.deserialize(json, valuesJson);
        } else {
            odm.deserialize(json);
        }
        return odm;
    }

    /**
     * This method deserializes the ODM from a JSON string.
     * When the valuesJson parameter is given, the hyperparameters are also deserialized.
     * @param json  The JSON string.
     * @param valuesJson The JSON string containing the hyperparameter values.
     */
    deserialize(json: any, valuesJson?: any): void {
        this.id = json.id;
        this.name = json.name.split('.')[1];
        if (valuesJson) {
            for (let param of json.hyper_parameters) {
                if(valuesJson[param.name] !== undefined){
                    this.hyperParameters.push(Hyperparameter.fromJSON(param, valuesJson));
                }
            }
        }
    }

    serialize(): string {
        return JSON.stringify(this);
    }
}