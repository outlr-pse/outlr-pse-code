import {Hyperparameter} from "./Hyperparameter";

/**
 *  HyperparameterType is an enum that represents the type of hyperparameter.
 */
export enum HyperparameterType {
    INTEGER = "integer",
    NUMERIC = "numeric",
    STRING = "string",
    BOOLEAN = "boolean",
}

export function getHyperparameterType(type: string): HyperparameterType {
    switch (type) {
        case "<class 'int'>":
            return HyperparameterType.INTEGER;
        case "<class 'float'>":
            return HyperparameterType.NUMERIC;
        case "<class 'str'>":
            return HyperparameterType.STRING;
        case "<class 'bool'>":
            return HyperparameterType.BOOLEAN;
        default:
            return HyperparameterType.STRING;
    }
}

export function validateHyperparameterType(param: Hyperparameter): boolean {
    switch (param.paramType) {
        case HyperparameterType.INTEGER:
            return !isNaN(parseInt(param.value));
        case HyperparameterType.NUMERIC:
            return !isNaN(parseFloat(param.value));
        case HyperparameterType.BOOLEAN:
            return param.value === "true" || param.value === "false";
        default:
            return true;
    }
}