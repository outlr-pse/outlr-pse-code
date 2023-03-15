import {SubspaceLogic} from "../../../src/models/subspacelogic/SubspaceLogic";
import {Operation} from "../../../src/models/subspacelogic/Operation";
import {Operator} from "../../../src/models/subspacelogic/Operator";
import {Literal} from "../../../src/models/subspacelogic/Literal";
import {Subspace} from "../../../src/models/results/Subspace";


describe("SubspaceLogic", () => {
    const subspace1 = new Subspace(1, "sub1", [1])
    const subspace1json = subspace1.serialize()
    const subspace2 = new Subspace(2, "sub2", [2, 3, 4])
    const subspace2json = subspace2.serialize()

    const logicJustLiteral = new Literal(subspace2)
    const logicJustLiteralJSON = `{"literal":{"subspace":${subspace2json}}}`

    const invalidLogicJSON= `{"literals":{"subspace":${subspace2json}}}`
    const invalidLogicJSON2= `{"literal":{"subspace":${subspace2json}}, "operation":{"operator":"and","operands":[{"literal":{"subspace":${subspace1json}}}}`

    const logicOneLayer = new Operation(
        Operator.AND,
        [ new Literal(subspace1), new Literal(subspace2) ],
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

    it("Serialize logic with just a literal", () => {
        expect(logicJustLiteral.serialize()).toBe(logicJustLiteralJSON)
    })

    it("Serialize logic with one layer", () => {
        expect(logicOneLayer.serialize()).toBe(logicOneLayerJSON)
    })

    it("Serialize logic with 3 layers", () => {
        expect(logicThreeLayer.serialize()).toBe(logicThreeLayerJSON)
    })

    it("Deserialize logic with just a literal", () => {
        expect(SubspaceLogic.fromJSON(logicJustLiteralJSON)).toEqual(logicJustLiteral)
    })

    it("Deserialize logic with one layer", () => {
        expect(SubspaceLogic.fromJSON(logicOneLayerJSON)).toEqual(logicOneLayer)
    })

    it("Deserialize logic with three layers", () => {
        expect(SubspaceLogic.fromJSON(logicThreeLayerJSON)).toEqual(logicThreeLayer)
    })

    it("no opearands", () => {
        expect(() => new Operation(Operator.AND, [])).toThrow()
    })
    it("unknown root", () => {
        expect(() => SubspaceLogic.fromJSON(invalidLogicJSON)).toThrow()
    })
    it("multiple keys", () => {
        expect(() => SubspaceLogic.fromJSON(invalidLogicJSON2)).toThrow()
    })
})