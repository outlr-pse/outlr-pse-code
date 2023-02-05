import {HyperparameterType} from "./HyperparameterType";
import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";

/**
 * This class represents a hyperparameter.
 */
export class Hyperparameter implements JSONSerializable, JSONDeserializable{
    name: string;
    value: string;
    type: HyperparameterType;

    constructor(name: string, value: string, type: HyperparameterType) {
        this.name = name;
        this.value = value;
        this.type = type;
    }

    /**
     * This method returns the hyperparameter as a JSON object.
     * It is called by the JSON.stringify() method.
     */
    toJSON() {
        return {
            name: this.name,
            value: this.value,
            type: this.type
        };
    }

    /**
     * This method creates a hyperparameter from a JSON string.
     * @param json
     */
    public static fromJSON(json: string): Hyperparameter {
        let hyperparameter = new Hyperparameter("", "", HyperparameterType.STRING);
        hyperparameter.deserialize(json);
        return hyperparameter;
    }

    deserialize(json: string): void {
        let jsonObject = JSON.parse(json);
        this.name = jsonObject.name;
        this.value = jsonObject.value;
        this.type = jsonObject.type;
    }

    serialize(): string {
        return JSON.stringify(this);
    }
}