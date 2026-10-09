// GameEvent Class - Event Object for Observer Pattern

public class GameEvent {

    // Event Type Enumeration
    public enum Type {
        EXP_CHANGED, // Player EXP Changed
        LIFE_LOST, // Player Lost a Life
        ITEM_COLLECTED, // Item Collected
        DOOR_CHOSEN, // Door Chosen
        MINIGAME_STARTED // Minigame Started
    }

    // Event Type
    private final Type type;

    // Event Data
    private final Object payload;

    // Constructor
    public GameEvent(Type type, Object payload) {
        this.type = type;
        this.payload = payload;
    }

    // Get Event Type
    public Type getType() {
        return type;
    }

    // Get Event Payload
    public Object getPayload() {
        return payload;
    }
}
