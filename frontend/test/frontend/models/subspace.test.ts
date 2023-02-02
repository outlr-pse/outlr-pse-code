// import { Outlier } from '../../../src/models/results/Outlier';
// import { Subspace } from '../../../src/models/results/Subspace';
// import subspaceJson from "../models/subspace.json";
//
// describe('Subspace', () => {
//     let subspace: Subspace;
//     let outlier: Outlier;
//
//     beforeEach(() => {
//         subspace = new Subspace(1,"exampleName", [1,2,3]);
//         outlier = new Outlier(1, [subspace]);
//         subspace.outliers = [outlier];
//         subspace.rocCurve = [{x: 1, y: 0.5}];
//     });
//
//      test('fromJSON', () => {
//          const deserializedSubspace = Subspace.fromJSON(subspaceJson.toString());
//          expect(deserializedSubspace).toEqual(subspace);
//      });
//
//      test('serialize', () => {
//          const serializedSubspace = subspace.serialize();
//          expect(serializedSubspace).toEqual(subspaceJson);
//     });
// });
