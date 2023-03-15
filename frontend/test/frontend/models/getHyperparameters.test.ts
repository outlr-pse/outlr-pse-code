import {Hyperparameter} from "../../../src/models/odm/Hyperparameter";
import {
    getHyperparameterType,
    HyperparameterType,
    validateHyperparameterType
} from "../../../src/models/odm/HyperparameterType";
import {ODM} from "../../../src/models/odm/ODM";


describe('getHyperparameters', () => {

    it.skip('should return list of hyperparameters', function () {
        const realHyperparameters = [
            new Hyperparameter(1, "hidden_activation", "", HyperparameterType.STRING, true),
            new Hyperparameter(2, "output_activation", "", HyperparameterType.STRING, true),
            new Hyperparameter(3, "loss", "", HyperparameterType.STRING, true),
            new Hyperparameter(4, "optimizer", "", HyperparameterType.STRING, false),
            new Hyperparameter(5, "epochs", "", HyperparameterType.INTEGER, true),
            new Hyperparameter(6, "batch_size", "", HyperparameterType.INTEGER, true),
            new Hyperparameter(7, "dropout_rate", "", HyperparameterType.NUMERIC, false),
            new Hyperparameter(8, "l2_regularizer", "", HyperparameterType.NUMERIC, true),
            new Hyperparameter(9, "validation_size", "", HyperparameterType.NUMERIC, true),
            new Hyperparameter(10, "preprocessing", "", HyperparameterType.BOOLEAN, false),
            new Hyperparameter(11, "verbose", "", HyperparameterType.INTEGER, true),
            new Hyperparameter(12, "contamination", "", HyperparameterType.NUMERIC, false)
        ];


        let jsonObject = JSON.parse("[{\"id\":1,\"name\":\"hidden_activation\",\"type\":\"string\",\"optional\":true},{\"id\":2,\"name\":\"output_activation\",\"type\":\"string\",\"optional\":true},{\"id\":3,\"name\":\"loss\",\"type\":\"string\",\"optional\":true},{\"id\":4,\"name\":\"optimizer\",\"type\":\"string\",\"optional\":false},{\"id\":5,\"name\":\"epochs\",\"type\":\"integer\",\"optional\":true},{\"id\":6,\"name\":\"batch_size\",\"type\":\"integer\",\"optional\":true},{\"id\":7,\"name\":\"dropout_rate\",\"type\":\"numeric\",\"optional\":false},{\"id\":8,\"name\":\"l2_regularizer\",\"type\":\"numeric\",\"optional\":true},{\"id\":9,\"name\":\"validation_size\",\"type\":\"numeric\",\"optional\":true},{\"id\":10,\"name\":\"preprocessing\",\"type\":\"boolean\",\"optional\":false},{\"id\":11,\"name\":\"verbose\",\"type\":\"integer\",\"optional\":true},{\"id\":12,\"name\":\"contamination\",\"type\":\"numeric\",\"optional\":false}]")
        let hyperparams = [];
        for (let paramJson of jsonObject) {
            hyperparams.push(Hyperparameter.fromJSON(paramJson))
        }
        expect(hyperparams).toEqual(realHyperparameters);
    });

    it.skip('should return list of odms', function () {
        const realODMs = [
            new ODM(1, "odm1", []),
            new ODM(2, "odm2", [])
        ];

        let jsonObject = JSON.parse("[{\"id\":1,\"name\":\"odm1\"},{\"id\":2,\"name\":\"odm2\"}]")
        let odms = [];
        for (let odmJson of jsonObject) {
            odms.push(ODM.fromJSON(odmJson))
        }
        expect(odms).toEqual(realODMs);

    });

    it('test validateHyperparameterType', function () {
        const StringParam = new Hyperparameter(1, "hidden_activation", "relu", HyperparameterType.STRING, true);
        const IntegerParam = new Hyperparameter(2, "epochs", "10", HyperparameterType.INTEGER, true);
        const NumericParam = new Hyperparameter(3, "dropout_rate", "0.1", HyperparameterType.NUMERIC, false);
        const BooleanParam = new Hyperparameter(4, "preprocessing", "true", HyperparameterType.BOOLEAN, false);
        const InvalidIntegerParam = new Hyperparameter(6, "epochs", "string", HyperparameterType.INTEGER, true);
        const InvalidNumericParam = new Hyperparameter(7, "dropout_rate", "string", HyperparameterType.NUMERIC, false);
        const InvalidBooleanParam = new Hyperparameter(8, "preprocessing", "20", HyperparameterType.BOOLEAN, false);
        expect(validateHyperparameterType(StringParam)).toBe(true);
        expect(validateHyperparameterType(IntegerParam)).toBe(true);
        expect(validateHyperparameterType(NumericParam)).toBe(true);
        expect(validateHyperparameterType(BooleanParam)).toBe(true);
        expect(validateHyperparameterType(InvalidIntegerParam)).toBe(false);
        expect(validateHyperparameterType(InvalidNumericParam)).toBe(false);
        expect(validateHyperparameterType(InvalidBooleanParam)).toBe(false);
    });

    it('test getHyperparameterType', function () {
        let stringType = getHyperparameterType("<class 'str'>");
        let integerType = getHyperparameterType("<class 'int'>");
        let numericType = getHyperparameterType("<class 'float'>");
        let booleanType = getHyperparameterType("<class 'bool'>");
        expect(stringType).toBe(HyperparameterType.STRING);
        expect(integerType).toBe(HyperparameterType.INTEGER);
        expect(numericType).toBe(HyperparameterType.NUMERIC);
        expect(booleanType).toBe(HyperparameterType.BOOLEAN);
    });

    it('test hyperparams in ODM to Json ', function () {
        let odm = new ODM(1, "odm1", []);
        let hyperparams = [
            new Hyperparameter(1, "hidden_activation", "relu", HyperparameterType.STRING, true),
            new Hyperparameter(2, "epochs", "10", HyperparameterType.INTEGER, true),
            new Hyperparameter(3, "dropout_rate", "0.1", HyperparameterType.NUMERIC, false),
            new Hyperparameter(4, "preprocessing", "true", HyperparameterType.BOOLEAN, false)
        ];
        odm.hyperParameters = hyperparams;
        let json = odm.toJSON();
        expect(json.hyper_parameters.hidden_activation).toBe("relu");
        expect(json.hyper_parameters.epochs).toBe(10);
        expect(json.hyper_parameters.dropout_rate).toBe(0.1);
        expect(json.hyper_parameters.preprocessing).toBe(1);

    });


});