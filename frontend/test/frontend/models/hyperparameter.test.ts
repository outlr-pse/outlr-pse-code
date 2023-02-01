import {Hyperparameter} from "../../../src/models/odm/Hyperparameter";
import {HyperparameterType} from "../../../src/models/odm/HyperparameterType";


describe('Hyperparameter', () => {
    let hyperparameter: Hyperparameter;

    beforeEach(() => {
        hyperparameter = new Hyperparameter('exampleName', 'exampleValue', HyperparameterType.STRING, false);
    });

    test('toJSON', () => {
        expect(hyperparameter.toJSON()).toEqual({
            name: 'exampleName',
            value: 'exampleValue',
            param_type: HyperparameterType.STRING,
            optional: false
        });
    });

    test('fromJSON', () => {
        const json = '{"name":"exampleName","value":"exampleValue","param_type":"string","optional":false}';
        const deserializedHyperparameter = Hyperparameter.fromJSON(json);
        expect(deserializedHyperparameter).toEqual(hyperparameter);
    });

    test('deserialize', () => {
        const json = '{"name":"newName","value":"newValue","param_type":"string","optional":false}';
        hyperparameter.deserialize(json);
        expect(hyperparameter).toEqual(new Hyperparameter('newName', 'newValue', HyperparameterType.STRING, false));
    });

    test('serialize', () => {
        const json = '{"name":"exampleName","value":"exampleValue","param_type":"string","optional":false}';
        expect(hyperparameter.serialize()).toEqual(json);
    });
});