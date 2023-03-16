import { getHyperparameterType, HyperparameterType } from './HyperparameterType'

/**
 * This class represents a hyperparameter.
 */
export class Hyperparameter {
  id: number
  name: string
  value: string
  paramType: HyperparameterType
  optional: boolean

  constructor (id: number, name: string, value: string, paramType: HyperparameterType, optional: boolean) {
    this.id = id
    this.name = name
    this.value = value
    this.paramType = paramType
    this.optional = optional
  }

  /**
     * This method creates a hyperparameter from a JSON string.
     * @param json The JSON string.
     * @param valuesJson The JSON string containing the hyperparameter values.
     */
  public static fromJSON (json: any, valuesJson?: any): Hyperparameter {
    const hyperparameter = new Hyperparameter(0, '', '', HyperparameterType.STRING, false)
    if (valuesJson) {
      hyperparameter.deserialize(json, valuesJson)
    } else {
      hyperparameter.deserialize(json)
    }
    return hyperparameter
  }

  /**
     * This method deserializes the Hyperparameter from a JSON string.
     * When the valuesJson parameter is given, th values of the hyperparameter are inserted.
     * @param json
     * @param valuesJson
     */
  deserialize (json: any, valuesJson?: any): void {
    this.id = json.id
    this.name = json.name
    this.paramType = getHyperparameterType(json.type)
    this.optional = json.optional
    if (valuesJson) {
      this.value = valuesJson[json.name]
    }
  }
}
