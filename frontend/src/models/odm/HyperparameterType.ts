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
        case "integer":
            return HyperparameterType.INTEGER;
        case "numeric":
            return HyperparameterType.NUMERIC;
        case "string":
            return HyperparameterType.STRING;
        case "boolean":
            return HyperparameterType.BOOLEAN;
        default:
            return HyperparameterType.STRING;
    }
}