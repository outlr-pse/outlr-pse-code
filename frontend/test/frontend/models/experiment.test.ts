import {Experiment} from '../../../src/models/experiment/Experiment';
import {ODM} from "../../../src/models/odm/ODM";
import {Subspace} from "../../../src/models/results/Subspace";
import {Literal} from "../../../src/models/subspacelogic/Literal";
import {Operation} from "../../../src/models/subspacelogic/Operation";
import {Operator} from "../../../src/models/subspacelogic/Operator";
import {ExperimentResult} from "../../../src/models/results/ExperimentResult";
import {Outlier} from "../../../src/models/results/Outlier";

describe('Experiment', () => {
    let experiment: Experiment;

    beforeEach(() => {
        experiment = new Experiment("name", "datasetName", null, null, new ODM("", []));

        const subspace1 = new Subspace(1, "sub1", [1])
        const subspace1json = subspace1.serialize()
        const subspace2 = new Subspace(2, "sub2", [2, 3, 4])
        const subspace2json = subspace2.serialize()

        const logicJustLiteral = new Literal(subspace2)
        const logicJustLiteralJSON = `{"literal":{"subspace":${subspace2json}}}`

        const logicOneLayer = new Operation(
            Operator.AND,
            [new Literal(subspace1), new Literal(subspace2)],
        )
        const logicOneLayerJSON = `{"operation":{"operator":"and","operands":[{"literal":{"subspace":${subspace1json}}},{"literal":{"subspace":${subspace2json}}}]}}`

        const logicTwoLayer = new Operation(
            Operator.AND,
            [logicOneLayer, new Literal(subspace2), new Literal(subspace1)]
        )
        const logicTwoLayerJSON = `{"operation":{"operator":"and","operands":[${logicOneLayerJSON},{"literal":{"subspace":${subspace2json}}},{"literal":{"subspace":${subspace1json}}}]}}`

        const logicThreeLayer = new Operation(
            Operator.AND,
            [logicOneLayer, logicTwoLayer, new Literal(subspace1)]
        )
        const logicThreeLayerJSON = `{"operation":{"operator":"and","operands":[${logicOneLayerJSON},${logicTwoLayerJSON},{"literal":{"subspace":${subspace1json}}}]}}`

        experiment.subspaceLogic = logicThreeLayer;

        let outliers = [

            new Outlier(1, [subspace1]),
            new Outlier(2, [subspace1, subspace2]),
            new Outlier(3, [subspace1]),
            new Outlier(4, [subspace2]),
            new Outlier(7, [subspace1, subspace2]),
            new Outlier(9, [subspace1]),
            new Outlier(10, [subspace2])
        ];

        subspace1.outliers = [outliers[0], outliers[1], outliers[2], outliers[4], outliers[5]]
        subspace2.outliers = [outliers[1], outliers[3], outliers[4], outliers[6]]

        let resultSpace = new Subspace(0, "resultSpace", []);
        resultSpace.outliers = outliers;


        experiment.experimentResult = new ExperimentResult(
            1,
            1,
            new Date(2000000000000),
            20,
            [subspace1, subspace2],
            outliers,
        )

        experiment.experimentResult.resultSpace = resultSpace;

    });

    it('should serialize', () => {
        const serialized = experiment.serialize();
        expect(serialized).toMatchSnapshot();
    });

});
