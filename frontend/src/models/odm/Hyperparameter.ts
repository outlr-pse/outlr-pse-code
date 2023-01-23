import {HyperparameterType} from "./HyperparameterType";
import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";

export class Hyperparameter implements JSONSerializable, JSONDeserializable{
    name: string;
    value: string;
    type: HyperparameterType;

    constructor(name: string, value: string, type: HyperparameterType) {
        this.name = name;
        this.value = value;
        this.type = type;
    }

    toJSON() {
        return {
            name: this.name,
            value: this.value,
            type: this.type
        };
    }

    //TODO: maybe den standart string type verändert wobei der eigentlich sofort überschrieben wird
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