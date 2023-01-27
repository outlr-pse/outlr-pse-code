import {Hyperparameter} from "../../../src/models/odm/Hyperparameter";
import {HyperparameterType} from "../../../src/models/odm/HyperparameterType";


describe('Hyperparameter', () => {
    let hyperparameter: Hyperparameter;

    beforeEach(() => {
        hyperparameter = new Hyperparameter('exampleName', 'exampleValue', HyperparameterType.STRING);
    });

    test('toJSON', () => {
        expect(hyperparameter.toJSON()).toEqual({
            name: 'exampleName',
            value: 'exampleValue',
            type: HyperparameterType.STRING
        });
    });

    test('fromJSON', () => {
        const json = '{"name":"exampleName","value":"exampleValue","type":"string"}';
        const deserializedHyperparameter = Hyperparameter.fromJSON(json);
        expect(deserializedHyperparameter).toEqual(hyperparameter);
    });

    test('deserialize', () => {
        const json = '{"name":"newName","value":"newValue","type":"string"}';
        hyperparameter.deserialize(json);
        expect(hyperparameter).toEqual(new Hyperparameter('newName', 'newValue', HyperparameterType.STRING));
    });

    test('serialize', () => {
        const json = '{"name":"exampleName","value":"exampleValue","type":"string"}';
        expect(hyperparameter.serialize()).toEqual(json);
    });
});