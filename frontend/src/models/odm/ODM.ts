import {Hyperparameter} from "./Hyperparameter";
import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";

/**
 * This class represents an ODM.
 */
export class ODM implements JSONSerializable, JSONDeserializable {
    name: string;
    hyperparameters: Hyperparameter[];

    constructor(name: string, hyperparameters: Hyperparameter[]) {
        this.name = name;
        this.hyperparameters = hyperparameters;
    }

    /**
     * This method returns the ODM as a JSON object.
     * It is called by the JSON.stringify() method.
     */
    toJSON() {
        return {
            name: this.name,
            hyperparameters: this.hyperparameters
        };
    }

    /**
     * This method creates an ODM from a JSON string.
     * @param json
     */
    public static fromJSON(json: string): ODM {
        let odm = new ODM("", []);
        odm.deserialize(json);
        return odm;
    }

    deserialize(json: string): void {
        let jsonObject = JSON.parse(json);
        this.name = jsonObject.name;
        this.hyperparameters = jsonObject.hyperparameters;
    }

    serialize(): string {
        return JSON.stringify(this);
    }
}