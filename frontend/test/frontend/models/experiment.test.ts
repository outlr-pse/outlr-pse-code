import {Experiment} from '../../../src/models/experiment/Experiment';
import {ODM} from "../../../src/models/odm/ODM";
import {Hyperparameter} from "../../../src/models/odm/Hyperparameter";
import {HyperparameterType} from "../../../src/models/odm/HyperparameterType";

describe('Experiment', () => {


    it('experiment from JSON',  () => {
        const serialized = "{\"id\":5,\"name\":\"ExampleExperiment\",\"dataset_name\":\"TestDataset\",\"odm\":{\"name\":\"copod.COPOD\",\"hyper_parameters\":[{\"name\":\"contamination\",\"type\":\"<class 'float'>\",\"optional\":true},{\"name\":\"n_jobs\",\"type\":\"<class 'int'>\",\"optional\":true}]},\"param_values\":{\"contamination\":0.1,\"n_jobs\":-1},\"experiment_result\":{\"running\":false,\"accuracy\":0.1,\"execution_date\":\"2019-01-01T00:00:00Z\",\"execution_time\":900}}"
        const experiment = Experiment.fromJSON(JSON.parse(serialized));
        expect(experiment.id).toBe(5);
        expect(experiment.name).toBe("ExampleExperiment");
        expect(experiment.datasetName).toBe("TestDataset");
        expect(experiment.odm.name).toBe("COPOD");
        expect(experiment.odm.hyperParameters.length).toBe(2);
        expect(experiment.odm.hyperParameters[0].name).toBe("contamination");
        expect(experiment.odm.hyperParameters[0].paramType).toBe("numeric");
        expect(experiment.odm.hyperParameters[0].optional).toBe(true);
        expect(experiment.odm.hyperParameters[0].value).toBe(0.1);
        expect(experiment.odm.hyperParameters[1].name).toBe("n_jobs");
        expect(experiment.odm.hyperParameters[1].paramType).toBe("integer");
        expect(experiment.odm.hyperParameters[1].optional).toBe(true);
        expect(experiment.odm.hyperParameters[1].value).toBe(-1);
        expect(experiment.running).toBe(false);
        expect(experiment.experimentResult?.accuracy).toBe(0.1);
        expect(experiment.experimentResult?.executionTime).toBe(900);
    })

    it('experimentResult from JSON',  () => {
        const serialized = "{\"id\":3,\"name\":\"ExampleExperiment\",\"dataset_name\":\"ExampleDataset\",\"odm\":{\"name\":\"COPOD\",\"hyper_parameters\":[{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":true},{\"name\":\"n_jobs\",\"type\":\"integer\",\"optional\":true}]},\"param_values\":{\"contamination\":0.1,\"n_jobs\":-1},\"subspace_logic\":{\"operation\":{\"operator\":\"or\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1,\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1,\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}}]}}]}},\"experiment_result\":{\"accuracy\":null,\"execution_date\":\"2018-01-01T00:00:00.000Z\",\"execution_time\":29,\"result_space\":{\"id\":13,\"name\":\"Result\",\"columns\":[],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}}"
        const deserialized = Experiment.fromJSON(JSON.parse(serialized));
        expect(deserialized).toBeInstanceOf(Experiment);
    })

    it('create experiment',  () => {
        let odm = new ODM(1,"lunar", []);
        odm.id = 14;
        odm.hyperParameters = [
            new Hyperparameter(15,"contamination", "value",HyperparameterType.NUMERIC, true),
            new Hyperparameter(36,"n_jobs","value2", HyperparameterType.INTEGER, true),
        ];
        const experiment = new Experiment(
          "exp1",
            "dataset1",
          null,
          null,
          odm,
      );
        const serialized = "{\"id\":3,\"name\":\"ExampleExperiment\",\"dataset_name\":\"ExampleDataset\",\"odm\":{\"name\":\"COPOD\",\"hyper_parameters\":[{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":true},{\"name\":\"n_jobs\",\"type\":\"integer\",\"optional\":true}]},\"param_values\":{\"contamination\":0.1,\"n_jobs\":-1},\"subspace_logic\":{\"operation\":{\"operator\":\"or\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1,\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1,\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}}]}}]}},\"experiment_result\":{\"accuracy\":null,\"execution_date\":\"2018-01-01T00:00:00.000Z\",\"execution_time\":29,\"result_space\":{\"id\":13,\"name\":\"Result\",\"columns\":[],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}}"
        const deserialized = Experiment.fromJSON(JSON.parse(serialized));
        experiment.subspaceLogic = deserialized.subspaceLogic;
        const experimentJson = experiment.serialize();
        expect(experimentJson).toBe(
            "{\"name\":\"exp1\",\"dataset\":null,\"dataset_name\":\"dataset1\",\"ground_truth\":null,\"odm\":{\"id\":14,\"hyper_parameters\":{\"15\":\"value\",\"36\":\"value2\"}},\"subspace_logic\":{\"operation\":{\"operator\":\"or\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1,\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1,\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}}]}}]}}}"
        )
    })

    it('mock files check if error occurs', () => {
        Experiment.fromJSON(JSON.parse("{\"id\":5,\"name\":\"ExampleExperiment\",\"dataset_name\":\"TestDataset\",\"odm\":{\"name\":\"COPOD\",\"hyper_parameters\":[{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":true},{\"name\":\"n_jobs\",\"type\":\"integer\",\"optional\":true}]},\"param_values\":{\"contamination\":0.1,\"n_jobs\":-1},\"experiment_result\":{\"id\":4,\"running\":false,\"accuracy\":0.1,\"execution_date\":\"2019-01-01T00:00:00Z\",\"execution_time\":900}}"))
        Experiment.fromJSON(JSON.parse("{\"id\":3,\"name\":\"ExampleExperiment\",\"dataset_name\":\"ExampleDataset\",\"odm\":{\"name\":\"COPOD\",\"hyper_parameters\":[{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":true},{\"name\":\"n_jobs\",\"type\":\"integer\",\"optional\":true}]},\"param_values\":{\"contamination\":0.1,\"n_jobs\":-1},\"subspace_logic\":{\"operation\":{\"operator\":\"or\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1,\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":1,\"name\":\"S1\",\"columns\":[2,3],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}}]}},{\"operation\":{\"operator\":\"and\",\"operands\":[{\"literal\":{\"subspace\":{\"id\":2,\"name\":\"S2\",\"columns\":[0,1,2,3],\"outliers\":[1,7,9,10,15,28,34],\"roc_curve\":null}}},{\"literal\":{\"subspace\":{\"id\":3,\"name\":\"S3\",\"columns\":[3,4,5],\"outliers\":[10,11,17,35],\"roc_curve\":null}}}]}}]}}]}},\"experiment_result\":{\"id\":3,\"accuracy\":null,\"execution_date\":\"2018-01-01T00:00:00.000Z\",\"execution_time\":29,\"result_space\":{\"id\":13,\"name\":\"Result\",\"columns\":[],\"outliers\":[9,10,15,28,34],\"roc_curve\":null}}}"))
        Experiment.fromJSON(JSON.parse("{\"id\":51,\"name\":\"ExampleExperiment2\",\"dataset_name\":\"TestDataset2\",\"odm\":{\"name\":\"HBOS\",\"hyper_parameters\":[{\"name\":\"n_bins\",\"type\":\"integer\",\"optional\":false},{\"name\":\"alpha\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"tol\",\"type\":\"numeric\",\"optional\":false},{\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]},\"param_values\":{\"n_bins\":10,\"alpha\":0.1,\"tol\":0.5,\"contamination\":0.1},\"experiment_result\":{\"id\":23,\"running\":false,\"accuracy\":0.97,\"execution_date\":\"2023-01-27T00:20:17.102Z\",\"execution_time\":20}}"))

    })

});
