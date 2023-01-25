/**
 * Interface for objects that can be serialized to JSON
 */
export interface JSONSerializable {
    /**
     * This method returns the object as a JSON object.
     */
    serialize(): string;

}