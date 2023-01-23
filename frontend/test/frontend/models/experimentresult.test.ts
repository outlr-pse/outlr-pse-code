import { Subspace } from '../../../src/models/results/Subspace';
import { Outlier } from '../../../src/models/results/Outlier';
import { ExperimentResult } from '../../../src/models/results/ExperimentResult';

describe('ExperimentResult', () => {
    let experimentResult: ExperimentResult;
    let subspace: Subspace;
    let outlier: Outlier;
    let executionDate: Date;

    beforeEach(() => {
        executionDate = new Date();
        outlier = new Outlier(1, [subspace]);
        subspace = new Subspace('exampleName', [1, 2, 3]);
        experimentResult = new ExperimentResult(1, 0.5, executionDate, 100, [subspace], [outlier]);
    });

    test('toJSON', () => {
        expect(experimentResult.toJSON()).toEqual({
            id: 1,
            accuracy: 0.5,
            executionDate: executionDate,
            executionTime: 100,
            subspaces: [subspace],
            outliers: [outlier]
        });
    });

    // test('fromJSON', () => {
    //     const json = '{"id":1,"accuracy":0.5,"executionDate":"'+ executionDate.toJSON()+'","executionTime":100,"subspaces":[{"name":"exampleName","columns":[1,2,3],"outliers":null,"rocCurve":null}],"outliers":[{"index":1,"subspaces":null}]}';
    //     const deserializedExperimentResult = ExperimentResult.fromJSON(json);
    //     expect(deserializedExperimentResult).toEqual(experimentResult);
    // });
    //
    // test('deserialize', () => {
    //     const json = '{"id":2,"accuracy":0.8,"executionDate":"'+ executionDate.toJSON()+'","executionTime":200,"subspaces":[{"name":"exampleName","columns":[1,2,3],"outliers":null,"rocCurve":null}],"outliers":[{"index":1,"subspaces":null}]}';
    //     experimentResult.deserialize(json);
    //     expect(experimentResult).toEqual(new ExperimentResult(2, 0.8, executionDate, 200, [subspace], [outlier]));
    // });
    //
    // test('serialize', () => {
    //     const json = '{"id":1,"accuracy":0.5,"executionDate":"'+ executionDate.toJSON()+'","executionTime":100,"subspaces":[{"name":"exampleName","columns":[1,2,3],"outliers":null,"rocCurve":null}],"outliers":[{"index":1,"subspaces":null}]}';
    //     expect(experimentResult.serialize()).toEqual(json);
    // });
});