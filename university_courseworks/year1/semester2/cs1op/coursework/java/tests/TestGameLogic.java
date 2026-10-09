// TestGameLogic class - logic and pattern tests

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestGameLogic {

    // Test Singleton Pattern
    @Test
    public void testGameSingletonInstance() {
        Game instance1 = Game.getInstance();
        Game instance2 = Game.getInstance();
        assertSame(instance1, instance2, "Game singleton should return same instance");
    }

    // Test Player Initialization
    @Test
    public void testPlayerInitialization() {
        Player player = new Player("TestPlayer");
        assertEquals("TestPlayer", player.getName());
        assertTrue(player.getExp() >= 0);
        assertEquals(3, player.getLives());
    }

    // Test EXP Management
    @Test
    public void testPlayerExpManagement() {
        Player player = new Player("TestPlayer");
        player.setExp(100);
        assertEquals(100, player.getExp());
        player.addExp(50);
        assertEquals(150, player.getExp());
        player.subtractExp(30);
        assertEquals(120, player.getExp());
    }

    // Test Lives Management
    @Test
    public void testPlayerLivesManagement() {
        Player player = new Player("TestPlayer");
        assertEquals(3, player.getLives());
        player.loseLife();
        assertEquals(2, player.getLives());
        player.loseLife();
        player.loseLife();
        assertEquals(0, player.getLives());
    }

    // Test Dice Roll
    @Test
    public void testDiceSystemRoll() {
        DiceSystem diceSystem = new DiceSystem();
        diceSystem.roll();
        int roll = diceSystem.getLastRoll();
        assertTrue(roll >= 1 && roll <= 6, "Dice roll should be between 1 and 6");
    }

    // Test HP Determination from Dice
    @Test
    public void testDiceSystemHPDetermination() {
        DiceSystem diceSystem = new DiceSystem();
        assertEquals(50, diceSystem.getHPFromRoll(1));
        assertEquals(50, diceSystem.getHPFromRoll(2));
        assertEquals(100, diceSystem.getHPFromRoll(3));
        assertEquals(100, diceSystem.getHPFromRoll(4));
        assertEquals(200, diceSystem.getHPFromRoll(5));
        assertEquals(200, diceSystem.getHPFromRoll(6));
    }

    // Test Door Factory Creation
    @Test
    public void testDoorFactoryCreation() {
        DoorFactory factory = new DoorFactory();
        Door door = factory.createRandomDoor(0);
        assertNotNull(door, "Factory should create a door instance");
    }

    // Test Reward Door Interaction
    @Test
    public void testRewardDoorInteraction() {
        Player player = new Player("TestPlayer");
        RewardDoor rewardDoor = new RewardDoor("Reward Door", "A shiny chest", 50);
        String result = rewardDoor.interact(player);
        assertNotNull(result);
        assertTrue(result.length() > 0, "RewardDoor interaction should return non-empty result");
    }

    // Test Penalty Door Interaction
    @Test
    public void testPenaltyDoorInteraction() {
        Player player = new Player("TestPlayer");
        PenaltyDoor penaltyDoor = new PenaltyDoor("Penalty Door", "A poison bottle", -25);
        String result = penaltyDoor.interact(player);
        assertNotNull(result);
        assertTrue(result.length() > 0, "PenaltyDoor interaction should return non-empty result");
    }

    // Test Minigame Door Properties
    @Test
    public void testMinigameDoorProperties() {
        MinigameDoor pongDoor = new MinigameDoor("Pong Door", "Table tennis court", "PONG");
        assertEquals("PONG", pongDoor.getGameType());
        assertEquals("Pong Door", pongDoor.getName());
    }

    // Test Door Properties
    @Test
    public void testDoorProperties() {
        Door door = new RewardDoor("Test Door", "Test Description", 100);
        assertEquals("Test Door", door.getName());
        assertEquals("Test Description", door.getDescription());
    }

    // Test Player Name Validation
    @Test
    public void testPlayerNameValidation() {
        Player player = new Player("TestPlayer");
        assertEquals("TestPlayer", player.getName());
        Player anotherPlayer = new Player("A");
        assertEquals("A", anotherPlayer.getName());
    }

    // Test EXP Edge Cases
    @Test
    public void testPlayerExpEdgeCases() {
        Player player = new Player("TestPlayer");
        player.setExp(0);
        assertEquals(0, player.getExp());
        player.setExp(500);
        assertEquals(500, player.getExp());
        player.addExp(1000);
        assertEquals(1500, player.getExp());
    }

    // Test Dice Roll Range Consistency
    @Test
    public void testDiceSystemRollRange() {
        DiceSystem diceSystem = new DiceSystem();
        for (int i = 0; i < 100; i++) {
            diceSystem.roll();
            int roll = diceSystem.getLastRoll();
            assertTrue(roll >= 1 && roll <= 6, "All rolls should be between 1 and 6");
        }
    }

    // Test Lives Edge Cases
    @Test
    public void testPlayerLivesEdgeCases() {
        Player player = new Player("TestPlayer");
        player.loseLife();
        player.loseLife();
        player.loseLife();
        player.loseLife();
        assertTrue(player.getLives() >= 0, "Lives should never go below 0");
    }

    // Test Game State Initialization
    @Test
    public void testGameStateInitialization() {
        Game game = Game.getInstance();
        game.initializePlayer("TestPlayer");
        assertNotNull(game);
        assertNotNull(game.getPlayer());
        assertEquals("TestPlayer", game.getPlayer().getName());
    }

    // Test Door Factory Variety
    @Test
    public void testDoorFactoryVariety() {
        DoorFactory factory = new DoorFactory();
        Door door1 = factory.createRandomDoor(0);
        Door door2 = factory.createRandomDoor(1);
        assertNotNull(door1);
        assertNotNull(door2);
    }

    // Test EXP Persistence
    @Test
    public void testPlayerExpPersistence() {
        Player player = new Player("TestPlayer");
        int initialExp = 150;
        player.setExp(initialExp);
        assertEquals(initialExp, player.getExp());
        player.loseLife();
        assertEquals(initialExp, player.getExp(), "EXP should persist after losing a life");
    }

    // Test Door String Representation
    @Test
    public void testDoorStringRepresentation() {
        Door door = new RewardDoor("Chest", "Golden chest", 75);
        String name = door.getName();
        String desc = door.getDescription();
        assertNotNull(name);
        assertTrue(name.length() > 0);
        assertNotNull(desc);
        assertTrue(desc.length() > 0);
    }

    // Test Maximum EXP
    @Test
    public void testPlayerMaximumEXP() {
        Player player = new Player("TestPlayer");
        player.setExp(10000);
        assertEquals(10000, player.getExp(), "Player should support large EXP values");
    }
}
