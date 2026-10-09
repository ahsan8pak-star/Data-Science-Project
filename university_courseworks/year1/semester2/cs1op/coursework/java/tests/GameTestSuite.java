// GameTestSuite class - comprehensive JUnit 5 test suite
// Tests Player class, DiceSystem, and Game logic

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class GameTestSuite {

    // Test player instance
    private Player player;

    // Test dice system instance
    private DiceSystem diceSystem;

    // Setup before each test
    @BeforeEach
    public void setUp() {
        player = new Player("TestPlayer");
        diceSystem = new DiceSystem();
    }

    // Test player initialization
    @Test
    public void testPlayerInitialization() {
        assertNotNull(player);
        assertEquals("TestPlayer", player.getName());
        assertEquals(3, player.getLives());
        assertEquals(0, player.getExp());
    }

    // Test EXP gain
    @Test
    public void testPlayerExpGain() {
        player.addExp(50);
        assertEquals(50, player.getExp());
        player.addExp(75);
        assertEquals(125, player.getExp());
    }

    // Test EXP penalty
    @Test
    public void testPlayerExpPenalty() {
        player.addExp(100);
        player.subtractExp(30);
        assertEquals(70, player.getExp());
    }

    // Test lose life
    @Test
    public void testPlayerLoseLife() {
        int initialLives = player.getLives();
        player.loseLife();
        assertEquals(initialLives - 1, player.getLives());
    }

    // Test game over when lives zero
    @Test
    public void testPlayerGameOverWhenLivesZero() {
        player.loseLife();
        player.loseLife();
        player.loseLife();
        assertEquals(0, player.getLives());
        assertTrue(player.isGameOver());
    }

    // Test set EXP
    @Test
    public void testPlayerSetExp() {
        player.setExp(200);
        assertEquals(200, player.getExp());
    }

    // Test dice roll range
    @Test
    public void testDiceRollRange() {
        int roll = diceSystem.roll();
        assertTrue(roll >= 1 && roll <= 6, "Dice roll should be between 1 and 6");
    }

    // Test HP assignment from dice roll
    @Test
    public void testDiceHPAssignment() {
        assertEquals(50, diceSystem.getHPFromRoll(1));
        assertEquals(50, diceSystem.getHPFromRoll(2));
        assertEquals(100, diceSystem.getHPFromRoll(3));
        assertEquals(100, diceSystem.getHPFromRoll(4));
        assertEquals(200, diceSystem.getHPFromRoll(5));
        assertEquals(200, diceSystem.getHPFromRoll(6));
    }

    // Test door bonus calculation
    @Test
    public void testDiceBonusCalculation() {
        assertEquals(50, diceSystem.getDoorBonusFromRoll(1, 50));
        assertEquals(100, diceSystem.getDoorBonusFromRoll(3, 50));
        assertEquals(200, diceSystem.getDoorBonusFromRoll(5, 50));
    }

    // Test last roll tracking
    @Test
    public void testDiceLastRollTracking() {
        diceSystem.roll();
        int lastRoll = diceSystem.getLastRoll();
        assertTrue(lastRoll >= 1 && lastRoll <= 6);
    }

    // Test dice ASCII art generation
    @Test
    public void testDiceASCIIArtGeneration() {
        for (int i = 1; i <= 6; i++) {
            diceSystem.roll();
            String ascii = diceSystem.getDiceFaceASCII();
            assertNotNull(ascii);
            assertFalse(ascii.isEmpty(), "Dice ASCII art should not be empty");
        }
    }

    // Test game win condition
    @Test
    public void testGameWinCondition() {
        player.setExp(500);
        assertTrue(player.getExp() >= 500, "Player should win with 500 EXP");
    }

    // Test game lose condition
    @Test
    public void testGameLoseConditionNegativeExp() {
        player.subtractExp(100);
        assertTrue(player.getExp() < 0, "EXP can go negative");
    }

    // Test EXP persists across life loss
    @Test
    public void testExperiencePersistenceAcrossLifeLoss() {
        player.setExp(250);
        int expBefore = player.getExp();
        player.loseLife();
        int expAfter = player.getExp();
        assertEquals(expBefore, expAfter, "EXP should persist after losing a life");
    }

    // Test reward door interaction
    @Test
    public void testRewardDoorInteraction() {
        RewardDoor door = new RewardDoor("Test Reward", "A test reward door", 50);
        String result = door.interact(player);
        assertNotNull(result);
        assertTrue(result.length() > 0);
    }

    // Test penalty door interaction
    @Test
    public void testPenaltyDoorInteraction() {
        PenaltyDoor door = new PenaltyDoor("Test Penalty", "A test penalty door", 25);
        String result = door.interact(player);
        assertNotNull(result);
        assertTrue(result.length() > 0);
    }

    // Test minigame door creation
    @Test
    public void testMinigameDoorCreation() {
        MinigameDoor door = new MinigameDoor("Test Minigame", "A test minigame door", "PONG");
        assertNotNull(door);
        assertEquals("PONG", door.getGameType());
    }

    // Test multiple lives loss
    @Test
    public void testMultipleLivesCost() {
        player.setExp(100);
        for (int i = 0; i < 3; i++) {
            player.loseLife();
        }
        assertEquals(0, player.getLives());
        assertEquals(100, player.getExp(), "EXP should remain unchanged");
    }

    // Test dice consistency
    @Test
    public void testDiceConsistency() {
        int sum = 0;
        for (int i = 0; i < 100; i++) {
            int roll = diceSystem.roll();
            sum += roll;
            assertTrue(roll >= 1 && roll <= 6);
        }
        assertTrue(sum > 200 && sum < 500, "Dice rolls should average around 3.5");
    }

    // Test maximum EXP
    @Test
    public void testPlayerMaxExp() {
        player.addExp(10000);
        assertEquals(10000, player.getExp());
    }

    // Test player name preservation
    @Test
    public void testPlayerNamePreservation() {
        String originalName = player.getName();
        player.addExp(100);
        player.loseLife();
        assertEquals(originalName, player.getName(), "Player name should remain unchanged");
    }
}