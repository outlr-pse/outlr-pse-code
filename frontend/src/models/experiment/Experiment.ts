import { type JSONDeserializable } from '../JSONDeserializable'
import { type JSONSerializable } from '../JSONSerializable'
import { ExperimentResult } from '../results/ExperimentResult'
import { ODM } from '../odm/ODM'
import { SubspaceLogic } from '../subspacelogic/SubspaceLogic'
import { type Subspace } from '../results/Subspace'
import { type Outlier } from '../results/Outlier'

/**
 * This class represents an experiment.
 */
export class Experiment implements JSONSerializable, JSONDeserializable {
  id: number | null
  name: string
  datasetName: string
  dataset: File | null
  groundTruth: File | null
  odm: ODM
  subspaceLogic: SubspaceLogic | null
  experimentResult: ExperimentResult | null
  running: boolean = false
  failed: boolean = false

  constructor (name: string,
    datasetName: string,
    dataset: File | null,
    groundTruth: File | null,
    odm: ODM,
    subspaceLogic?: SubspaceLogic) {
    this.id = null
    this.name = name
    this.datasetName = datasetName
    this.dataset = dataset
    this.groundTruth = groundTruth
    this.odm = odm
    this.subspaceLogic = subspaceLogic != undefined ? subspaceLogic : null
    this.experimentResult = null
    this.running = false
  }

  /**
     * This method returns the experiment as a JSON object.
     * It is called by the JSON.stringify() method.
     */
  toJSON () {
    return {
      name: this.name,
      dataset: this.dataset,
      dataset_name: this.datasetName,
      ground_truth: this.groundTruth,
      odm: this.odm,
      subspace_logic: this.subspaceLogic
    }
  }

  /**
     * This method creates an experiment from a JSON string.
     * @param json
     */
  public static fromJSON (json: any): Experiment {
    const experiment = new Experiment('', '', null, null, new ODM(0, '', []))
    experiment.deserialize(json)
    return experiment
  }

  /**
     * This method deserializes the experiment from a JSON string.
     * When the experiment result is given, the experiment is not running anymore.
     * @param json The JSON string.
     */
  deserialize (json: any): void {
    this.id = json.id
    this.name = json.name
    this.datasetName = json.dataset_name
    this.odm = ODM.fromJSON(json.odm, json.odm_params)

    const subspaceMap = new Map<number, Subspace>()
    const outlierMap = new Map<number, Outlier>()

    if (json.error_json) {
      this.failed = true
    }
    if (json.subspace_logic != null) {
      this.subspaceLogic = SubspaceLogic.fromJSONObject(json.subspace_logic, subspaceMap, outlierMap)
    } else {
      this.subspaceLogic = null
    }
    if (json.experiment_result != undefined) {
      this.experimentResult = ExperimentResult.fromJSONObject(json.experiment_result, subspaceMap, outlierMap)
      this.running = false
    } else {
      this.running = true
    }
  }

  serialize (): string {
    return JSON.stringify(this)
  }
}
