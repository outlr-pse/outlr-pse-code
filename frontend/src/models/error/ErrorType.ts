/**
 * This enum represents an ErrorType.
 * The string that is mapped to each enum entry is used by the API to classify the error
 */
export enum ErrorType {
    /** An error, which has to do with JWT access tokens and operation */
    JWTAuthError = "JWTAuthError",
    /** An error in the user management part of the API */
    UserManagementError = "UserManagementError",
    /** An error in the experiment part of the API */
    ExperimentError = "ExperimentError",
    /** An error in the ODM part of the API */
    ODMError = "ODMError",
    /**An error of other origin */
    OtherError = "OtherError"
}