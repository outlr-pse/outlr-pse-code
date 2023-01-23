import { Outlier } from '../../../src/models/results/Outlier';
import { Subspace } from '../../../src/models/results/Subspace';

describe('Subspace', () => {
    let subspace: Subspace;
    let outlier: Outlier;

    beforeEach(() => {
        outlier = new Outlier(1, [subspace]);
        subspace = new Subspace('exampleName', [1, 2, 3]);
        subspace.outliers = [outlier];
        subspace.rocCurve = [{x: 1, y: 0.5}];
    });

    test('toJSON', () => {
        expect(subspace.toJSON()).toEqual({
            name: 'exampleName',
            columns: [1, 2, 3],
            outliers: [outlier],
            rocCurve: [{x: 1, y: 0.5}]
        });
    });

    // test('fromJSON', () => {
    //     const json = '{"name":"exampleName","columns":[1,2,3],"outliers":[{"index":1,"subspaces":[{"name":"exampleName","columns":[1,2,3],"outliers":null,"rocCurve":null}]}],"rocCurve":[{"x":1,"y":0.5}]}';
    //     const deserializedSubspace = Subspace.fromJSON(json);
    //     expect(deserializedSubspace).toEqual(subspace);
    // });
    //
    // test('serialize', () => {
    //     const json = '{"name":"exampleName","columns":[1,2,3],"outliers":[{"index":1,"subspaces":[{"name":"exampleName","columns":[1,2,3],"outliers":null,"rocCurve":null}]}],"rocCurve":[{"x":1,"y":0.5}]}';
    //     expect(subspace.serialize()).toEqual(json);
    // });
});
