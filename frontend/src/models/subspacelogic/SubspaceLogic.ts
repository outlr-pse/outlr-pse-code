import {JSONDeserializable} from "../JSONDeserializable";
import {JSONSerializable} from "../JSONSerializable";

export interface SubspaceLogic extends JSONSerializable, JSONDeserializable {
    constructor(json: string): void;
    serialize(): string;
    deserialize(json: string): void;

}