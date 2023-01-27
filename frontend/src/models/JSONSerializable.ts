/**
 * This interface provides the functionality of serializing an object to JSON
 */
export interface JSONSerializable {
    /**
     * Serialize object. Returns json as a string.
     */
    serialize(): string;

}