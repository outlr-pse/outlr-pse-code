import {JSONSerializable} from "../JSONSerializable";
import {JSONDeserializable} from "../JSONDeserializable";

export class User  implements JSONSerializable, JSONDeserializable {
    username: string;
    password: string;

    constructor(username: string, password: string){
        this.username = username;
        this.password = password;
    }

    public static fromJSON(json: string): User {
        let user = new User("", "");
        user.deserialize(json);
        return user;
    }

    toJSON() {
        return {
            username: this.username,
            password: this.password
        };
    }

    deserialize(json: string): void {
        let jsonObject = JSON.parse(json);
        this.username = jsonObject.username;
        this.password = jsonObject.password;
    }

    serialize(): string {
        return JSON.stringify(this);
    }


}