import { Hyperparameter} from '../../../src/models/odm/Hyperparameter';
import { ODM } from '../../../src/models/odm/ODM';
import {HyperparameterType} from "../../../src/models/odm/HyperparameterType";

describe('ODM', () => {
    let odm: ODM;
    let hyperparameter1: Hyperparameter;
    let hyperparameter2: Hyperparameter;

    beforeEach(() => {
        hyperparameter1 = new Hyperparameter('exampleName1', 'exampleValue1', HyperparameterType.STRING);
        hyperparameter2 = new Hyperparameter('exampleName2', 'exampleValue2', HyperparameterType.STRING);
        odm = new ODM('exampleName', [hyperparameter1, hyperparameter2]);
    });

    test('toJSON', () => {
        expect(odm.toJSON()).toEqual({
            name: 'exampleName',
            hyperparameters: [hyperparameter1, hyperparameter2]
        });
    });

    test('fromJSON', () => {
        const json = '{"name":"exampleName","hyperparameters":[{"name":"exampleName1","value":"exampleValue1","type":"string"},{"name":"exampleName2","value":"exampleValue2","type":"string"}]}';
        const deserializedOdm = ODM.fromJSON(json);
        expect(deserializedOdm).toEqual(odm);
    });

    test('deserialize', () => {
        const json = '{"name":"newName","hyperparameters":[{"name":"exampleName1","value":"exampleValue1","type":"string"},{"name":"exampleName2","value":"exampleValue2","type":"string"}]}';
        odm.deserialize(json);
        expect(odm).toEqual(new ODM('newName', [hyperparameter1, hyperparameter2]));
    });

    test('serialize', () => {
        const json = '{"name":"exampleName","hyperparameters":[{"name":"exampleName1","value":"exampleValue1","type":"string"},{"name":"exampleName2","value":"exampleValue2","type":"string"}]}';
        expect(odm.serialize()).toEqual(json);
    });
});
