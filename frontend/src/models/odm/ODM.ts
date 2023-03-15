import { Hyperparameter } from './Hyperparameter'
import { type JSONSerializable } from '../JSONSerializable'
import { HyperparameterType } from './HyperparameterType'

/**
 * This class represents an ODM.
 */
export class ODM implements JSONSerializable {
  id: number
  name: string
  hyperParameters: Hyperparameter[]

  constructor (id: number, name: string, hyperParameters: Hyperparameter[]) {
    this.id = id
    this.name = name
    this.hyperParameters = hyperParameters
  }

  /**
     * This method returns the ODM as a JSON object.
     * It is called by the JSON.stringify() method.
     */
  toJSON () {
    const hyperParametersJSON: Record<string, any> = {}
    for (const param of this.hyperParameters) {
      if (param.value !== '') {
        if (param.paramType === HyperparameterType.BOOLEAN) { hyperParametersJSON[param.name] = param.value === 'true' ? 1 : 0 } else if (param.paramType === HyperparameterType.INTEGER) {
          hyperParametersJSON[param.name] = parseInt(param.value)
        } else if (param.paramType === HyperparameterType.NUMERIC) {
          hyperParametersJSON[param.name] = parseFloat(param.value)
        } else {
          hyperParametersJSON[param.name] = param.value
        }
      }
    }
    return {
      id: this.id,
      hyper_parameters: hyperParametersJSON
    }
  }

  /**
     * This method creates an ODM from a JSON string.
     * @param json The JSON string.
     * @param valuesJson The JSON string containing the hyperparameter values.
     */
  public static fromJSON (json: any, valuesJson?: any): ODM {
    const odm = new ODM(0, '', [])
    if (valuesJson) {
      odm.deserialize(json, valuesJson)
    } else {
      odm.deserialize(json)
    }
    return odm
  }

  /**
     * This method deserializes the ODM from a JSON string.
     * When the valuesJson parameter is given, the hyperparameters are also deserialized.
     * @param json  The JSON string.
     * @param valuesJson The JSON string containing the hyperparameter values.
     */
  deserialize (json: any, valuesJson?: any): void {
    this.id = json.id
    this.name = json.name.split('.')[1]
    if (valuesJson) {
      for (const param of json.hyper_parameters) {
        if (valuesJson[param.name] !== undefined) {
          this.hyperParameters.push(Hyperparameter.fromJSON(param, valuesJson))
        }
      }
    }
  }

  serialize (): string {
    return JSON.stringify(this)
  }
}
