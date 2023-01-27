import {ExperimentResult} from '../../../src/models/results/ExperimentResult';
import {Subspace} from '../../../src/models/results/Subspace';
import {Outlier} from '../../../src/models/results/Outlier';

describe('ExperimentResult', () => {
    let subspaces: Subspace[];
    let outliers: Outlier[];
    let experimentResult: ExperimentResult;
    let subspaceMap: Map<number, Subspace>;
    let outlierMap: Map<number, Outlier>;
    let resultSpace: Subspace | undefined;

    beforeEach(() => {
        subspaces = [
            new Subspace(1, "exampleName1", [1, 2, 3]),
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

        subspaceMap = new Map<number, Subspace>();
        subspaceMap.set(1, subspaces[0]);
        subspaceMap.set(2, subspaces[1]);

        outlierMap = new Map<number, Outlier>();
        for (let outlier of outliers) {
            outlierMap.set(outlier.index, outlier);
        }

        resultSpace = new Subspace(0, "resultSpace", []);
        resultSpace.outliers = outliers;

        experimentResult = new ExperimentResult(1, 0.9, new Date(2000000), 100, subspaces, outliers, resultSpace)
    });

    test('should create an instance of ExperimentResult', () => {
        expect(experimentResult).toBeInstanceOf(ExperimentResult);
    });

    test('should serialize and deserialize correctly', () => {
        const serialized = experimentResult.serialize();
        const deserialized = ExperimentResult.fromJSONObject(JSON.parse(serialized), subspaceMap, outlierMap);
        expect(deserialized).toEqual(experimentResult);
    });

    test('should return the correct JSON object', () => {
        const json = experimentResult.toJSON();
        expect(json).toEqual({
            id: 1,
            accuracy: 0.9,
            executionDate: experimentResult.executionDate,
            executionTime: 100,
            resultSpace: resultSpace
        });
    });
});