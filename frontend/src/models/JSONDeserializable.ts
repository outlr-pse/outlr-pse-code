/**
 * This interface provides the functionality of deserializing an object from JSON.
 */
export  interface JSONDeserializable {
    /**
     * Deserialize from JSON. This overrides the current object.
     * @param json
     */
    deserialize(json: string): void;
}