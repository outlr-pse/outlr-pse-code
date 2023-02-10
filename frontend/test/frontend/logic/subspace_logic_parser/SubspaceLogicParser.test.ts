import {parseSubspaceLogic} from "../../../../src/logic/subspace_logic_parser/SubspaceLogicParser";
import {Literal} from "../../../../src/models/subspacelogic/Literal";
import {Operation} from "../../../../src/models/subspacelogic/Operation";
import {Operator} from "../../../../src/models/subspacelogic/Operator";
import {SubspaceLogic} from "../../../../src/models/subspacelogic/SubspaceLogic";
import {Subspace} from "../../../../src/models/results/Subspace";

function expectSubspaceLogicToBeEqual(actual: SubspaceLogic | null, expected: SubspaceLogic) {
    if (expected instanceof Literal)
        expectLiteral(actual, expected)
    else if (expected instanceof Operation)
        expectOperation(actual, expected)
    else
        throw new Error("Unexpected case")
}

function expectLiteral(actual: SubspaceLogic | null, expected: Literal) {
    expect(actual !== null).toBeTruthy()
    if (actual === null) return
    expect(actual instanceof Literal).toBeTruthy()
    if (!(actual instanceof Literal)) return
    expect(actual.subspace.columns).toEqual(expected.subspace.columns)
}

function expectOperation(actual: SubspaceLogic | null, expected: Operation) {
    expect(actual !== null).toBeTruthy()
    if (actual === null) return
    expect(actual instanceof Operation).toBeTruthy()
    if (!(actual instanceof Operation)) return
    expect(actual.operator).toEqual(expected.operator)
    expect(actual.operands.length).toEqual(expected.operands.length)
    for (let i = 0; i < expected.operands.length; i++) {
        expectSubspaceLogicToBeEqual(actual.operands[i], expected.operands[i])
    }
}

describe("SubspaceLogicParser", () => {

    it("Test single literal", () => {
        let input = "[0, 1, 32]"
        let logic = parseSubspaceLogic(input)
        expectLiteral(logic, new Literal(new Subspace(null, null, [0, 1, 32])))
    })

     it("Test single literal in bad format", () => {
        let input = "  [ 0 ,1,32   ,   1, 1, 1, 1  ]        "
        let logic = parseSubspaceLogic(input)
        expectLiteral(logic, new Literal(new Subspace(null, null, [0, 1, 32, 1, 1, 1, 1])))
    })

    it("Test operation with 2 operands", () => {
        let input = "[0, 1] and [1, 2]"
        let logic = parseSubspaceLogic(input)
        expectOperation(
            logic,
            new Operation(Operator.AND, [
                new Literal(new Subspace(null, null, [0, 1])),
                new Literal(new Subspace(null, null, [1, 2])),
            ])
        )
    })

    it("Test operation with 2 operands in bad format", () => {
        let input = "    [0,1 ]    or[1,2      ]             "
        let logic = parseSubspaceLogic(input)
        expectOperation(
            logic,
            new Operation(Operator.OR, [
                new Literal(new Subspace(null, null, [0, 1])),
                new Literal(new Subspace(null, null, [1, 2])),
            ])
        )
    })

    it("Test subspace logic with multiple operands", () => {
        let input = "[0, 1] and [1, 43] or [2, 32, 0] or [3] and [4]"
        let logic = parseSubspaceLogic(input)
        console.log(logic?.serialize())
        expectOperation(
            logic,
            new Operation(Operator.AND, [
                new Literal(new Subspace(null, null, [0, 1])),
                new Operation(Operator.OR, [
                    new Literal(new Subspace(null, null, [1,43])),
                    new Operation(Operator.OR, [
                        new Literal(new Subspace(null, null, [2, 32, 0])),
                        new Operation(Operator.AND, [
                            new Literal(new Subspace(null, null, [3])),
                            new Literal(new Subspace(null, null, [4])),
                        ]),
                    ]),
                ]),
            ])
        )
    })

    it("Test subspace logic with multiple operands in bad format", () => {
        let input = "[0,1]and[1,     43  ]or[   2   ,32,0  ]or     [3  ]  and[ 4] "
        let logic = parseSubspaceLogic(input)
        console.log(logic?.serialize())
        expectOperation(
            logic,
            new Operation(Operator.AND, [
                new Literal(new Subspace(null, null, [0, 1])),
                new Operation(Operator.OR, [
                    new Literal(new Subspace(null, null, [1,43])),
                    new Operation(Operator.OR, [
                        new Literal(new Subspace(null, null, [2, 32, 0])),
                        new Operation(Operator.AND, [
                            new Literal(new Subspace(null, null, [3])),
                            new Literal(new Subspace(null, null, [4])),
                        ]),
                    ]),
                ]),
            ])
        )
    })

})