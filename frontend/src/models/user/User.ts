import {JSONSerializable} from "../JSONSerializable";
import {JSONDeserializable} from "../JSONDeserializable";

export class User implements JSONDeserializable, JSONSerializable {
    username: string;
    password: string;

    constructor(username: string, password: string){
        this.username = username;
        this.password = password;
    }

    public static fromJSON(json: string): User {

        return new;
    }

    deserialize(json: string): void {
        // deserialization logic here
        // this.username = ...
        // this.password = ...
    }

    serialize(): string {

        return "";
    }


}