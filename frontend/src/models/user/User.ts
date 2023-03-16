import { type JSONSerializable } from '../JSONSerializable'
import { type JSONDeserializable } from '../JSONDeserializable'

/**
 * This class represents a user.
 */
export class User implements JSONSerializable, JSONDeserializable {
  username: string
  password: string

  constructor (username: string, password: string) {
    this.username = username
    this.password = password
  }

  /**
     * This method returns the user as a JSON object.
     * @param json
     */
  public static fromJSON (json: string): User {
    const user = new User('', '')
    user.deserialize(json)
    return user
  }

  /**
     * This method returns the user as a JSON object.
     * It is called by the JSON.stringify() method.
     */
  toJSON (): any {
    return {
      username: this.username,
      password: this.password
    }
  }

  deserialize (json: string): void {
    const jsonObject = JSON.parse(json)
    this.username = jsonObject.username
    this.password = jsonObject.password
  }

  serialize (): string {
    return JSON.stringify(this)
  }
}
