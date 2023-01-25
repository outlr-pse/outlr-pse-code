/**
 * Interface for deserializing JSON data.
 */
export  interface JSONDeserializable {
    /**
     * This method creates an object from a JSON string.
     * @param json
     */
    deserialize(json: string): void;
}