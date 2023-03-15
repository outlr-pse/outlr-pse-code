import { Outlier } from './Outlier'
import { type JSONSerializable } from '../JSONSerializable'

/**
 * This class represents a subspace.
 */
export class Subspace implements JSONSerializable {
  id: number | null
  name: string | null
  columns: number[]
  outliers: Outlier[] | null
  rocCurve: Array<Record<any, any>> | null

  constructor (id: number | null, name: string | null,
    columns: number[]) {
    this.id = id
    this.name = name
    this.columns = columns
    this.outliers = []
    this.rocCurve = null
  }

  /**
     * This method returns the subspace as a JSON object.
     * It is called by the JSON.stringify() method.
     */
  toJSON () {
    const outlierIndices = []
    if (this.outliers != null) {
      for (const outlier of this.outliers) {
        outlierIndices.push(outlier.index)
      }
    }
    return {
      id: this.id,
      name: this.name,
      columns: this.columns,
      outliers: outlierIndices,
      roc_curve: this.rocCurve
    }
  }

  serialize (): string {
    return JSON.stringify(this)
  }

  /**
     * This method creates a subspace from a JSON object.
     * @param jsonObject The JSON object.
     * @param outlierMap The map of outliers to check if outlier already exist.
     * After the subspace is created, the outliers are added to the outlier map.
     */
  static fromJSONObject (jsonObject: any, outlierMap: Map<number, Outlier>): Subspace {
    const newSubspace = new Subspace(jsonObject.id, jsonObject.name, jsonObject.columns)
    newSubspace.rocCurve = jsonObject.roc_curve
    newSubspace.outliers = []
    for (const jsonOutlier of jsonObject.outliers) {
      let outlier = null
      if (outlierMap.has(jsonOutlier)) {
        outlier = outlierMap.get(jsonOutlier) as Outlier
      } else {
        outlier = new Outlier(jsonOutlier, [])
        outlierMap.set(jsonOutlier, outlier)
      }
      outlier.subspaces.push(newSubspace)
      newSubspace.outliers.push(outlier)
    }
    return newSubspace
  }
}
