import { type JSONSerializable } from '../JSONSerializable'
import { Subspace } from './Subspace'
import { type Outlier } from './Outlier'

/**
 * This class represents an experiment result.
 */
export class ExperimentResult implements JSONSerializable {
  accuracy: number
  executionDate: Date
  executionTime: number
  subspaces: Subspace[]
  outliers: Outlier[]
  resultSpace: Subspace | undefined

  constructor (accuracy: number,
    executionDate: Date,
    executionTime: number,
    subspaces: Subspace[],
    outliers: Outlier[],
    resultSpace?: Subspace) {
    this.accuracy = accuracy
    this.executionDate = executionDate
    this.executionTime = executionTime
    this.subspaces = subspaces
    this.outliers = outliers
    this.resultSpace = resultSpace
  }

  serialize (): string {
    return JSON.stringify(this)
  }

  /**
     * This method creates an experiment result from a JSON object.
     * @param jsonObject The JSON object.
     * @param subspaceMap The map of all subspaces that the experiment holds.
     * @param outlierMap The map of  all outliers that the experiment holds.
     */
  static fromJSONObject (jsonObject: any, subspaceMap: Map<number, Subspace>, outlierMap: Map<number, Outlier>): ExperimentResult {
    let resultSpace
    if (jsonObject.result_space !== undefined) {
      resultSpace = Subspace.fromJSONObject(jsonObject.result_space, outlierMap)
    }

    return new ExperimentResult(
      jsonObject.accuracy,
      new Date(jsonObject.execution_date),
      jsonObject.execution_time,
      Array.from(subspaceMap.values()),
      Array.from(outlierMap.values()),
      resultSpace
    )
  }
}
