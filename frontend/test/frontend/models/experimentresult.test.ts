import {ExperimentResult} from '../../../src/models/results/ExperimentResult';
import {Subspace} from '../../../src/models/results/Subspace';
import {Outlier} from '../../../src/models/results/Outlier';

describe('ExperimentResult', () => {
    let subspaces: Subspace[];
    let outliers: Outlier[];
    let experimentResult: ExperimentResult;

    beforeEach(() => {
        subspaces = [
            new Subspace(1, "exampleName1" ,[1, 2, 3]),
            new Subspace(2, "exampleName2", [4, 5, 6])
        ];
        outliers = [

            new Outlier(1, [subspaces[0]]),
            new Outlier(2, [subspaces[0], subspaces[1]]),
            new Outlier(3, [subspaces[0]]),
            new Outlier(4, [subspaces[1]]),
            new Outlier(7, [subspaces[0], subspaces[1]]),
            new Outlier(9, [subspaces[0]]),
            new Outlier(10, [subspaces[1]])
        ];
        subspaces[0].outliers = [outliers[0], outliers[1], outliers[2], outliers[4], outliers[5]];
        subspaces[1].outliers = [outliers[1], outliers[3], outliers[4], outliers[6]];

        experimentResult = new ExperimentResult(1, 0.9, new Date(), 100, subspaces, outliers);
    });

    test('should create an instance of ExperimentResult', () => {
        expect(experimentResult).toBeInstanceOf(ExperimentResult);
    });

    test('should serialize and deserialize correctly', () => {
        const serialized = experimentResult.serialize();
        const deserialized = ExperimentResult.fromJSON(serialized);
        expect(deserialized).toEqual(experimentResult);
    });

    test('should return the correct JSON object', () => {
        const json = experimentResult.toJSON();
        expect(json).toEqual({
            id: 1,
            accuracy: 0.9,
            executionDate: experimentResult.executionDate,
            executionTime: 100,
            subspaces: subspaces,
            outliers: [1,2,3,4,7,9,10]
        });
    });
});