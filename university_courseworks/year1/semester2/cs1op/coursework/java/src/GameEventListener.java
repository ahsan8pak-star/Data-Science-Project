// GameEventListener Interface - Observer Pattern
// Implementations Receive Game Events

public interface GameEventListener {

    // Called when a game event occurs
    void onEvent(GameEvent event);
}
