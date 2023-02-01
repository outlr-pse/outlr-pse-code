import {HyperparameterType} from "./HyperparameterType";
import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";

/**
 * This class represents a hyperparameter.
 */
export class Hyperparameter implements JSONSerializable, JSONDeserializable{
    name: string;
    value: string;
    paramType: HyperparameterType;
    optional: boolean;

    constructor(name: string, value: string, paramType: HyperparameterType, optional: boolean) {
        this.name = name;
        this.value = value;
        this.paramType = paramType;
        this.optional = optional;
    }

    /**
     * This method returns the hyperparameter as a JSON object.
     * It is called by the JSON.stringify() method.
     */
    toJSON() {
        return {
            name: this.name,
            value: this.value,
            param_type: this.paramType,
            optional: this.optional
        };
    }

    /**
     * This method creates a hyperparameter from a JSON string.
     * @param json
     */
    public static fromJSON(json: string): Hyperparameter {
        let hyperparameter = new Hyperparameter("", "", HyperparameterType.STRING, false);
        hyperparameter.deserialize(json);
        return hyperparameter;
    }

    deserialize(json: string): void {
        let jsonObject = JSON.parse(json);
        this.name = jsonObject.name;
        this.value = jsonObject.value;
        this.paramType = jsonObject.param_type
        this.optional = jsonObject.optional;
    }

    serialize(): string {
        return JSON.stringify(this);
    }
}