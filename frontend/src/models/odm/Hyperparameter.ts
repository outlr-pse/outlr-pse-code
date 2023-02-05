import {HyperparameterType} from "./HyperparameterType";
import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";

/**
 * This class represents a hyperparameter.
 */
export class Hyperparameter{
    id: number;
    name: string;
    value: string;
    paramType: HyperparameterType;
    optional: boolean;

    constructor(id: number, name: string, value: string, paramType: HyperparameterType, optional: boolean) {
        this.id = id;
        this.name = name;
        this.value = value;
        this.paramType = paramType;
        this.optional = optional;
    }


    /**
     * This method creates a hyperparameter from a JSON string.
     * @param json
     * @param valuesJson
     */
    public static fromJSON(json: any, valuesJson: any): Hyperparameter {
        let hyperparameter = new Hyperparameter(0,"", "", HyperparameterType.STRING, false);
        hyperparameter.deserializeParam(json, valuesJson);
        return hyperparameter;
    }

    deserializeParam(json: any, valuesJson: any): void {
        this.name = json.name;
        this.paramType = json.type
        this.optional = json.optional;
        this.value = valuesJson[json.name];
    }
}