// ManualTestRunner - simple test runner without external dependencies
// Run with: java -cp bin tests.ManualTestRunner

public class ManualTestRunner {

    private static int passed = 0;
    private static int failed = 0;
    private static int total = 0;

    public static void main(String[] args) {
        System.out.println("=".repeat(50));
        System.out.println("CS1OP Manual Test Runner");
        System.out.println("=".repeat(50));
        System.out.println();

        total++;
        if (testPlayerInitialization()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testPlayerAddExp()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testPlayerAddItem()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testDoorFactoryCreatesDoor()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testDoorInteractionReturnsResult()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testResourcesFileExists()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testGameSingletonInstance()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testPlayerLivesManagement()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testDiceSystemRoll()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testDiceSystemHPDetermination()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testDoorFactoryVariety()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testPlayerExpPersistence()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testRewardDoorInteraction()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testPenaltyDoorInteraction()) {
            passed++;
        } else {
            failed++;
        }
        total++;
        if (testMinigameDoorProperties()) {
            passed++;
        } else {
            failed++;
        }

        System.out.println();
        System.out.println("=".repeat(50));
        System.out.println("RESULTS: " + total + " tests, " + passed + " passed, " + failed + " failed");
        System.out.println("=".repeat(50));

        if (failed > 0) {
            System.exit(1);
        }
    }

    private static boolean testPlayerInitialization() {
        try {
            Player p = new Player("Tester", 100);
            return assertEquals(100, p.getExp(), "Player initialization with EXP")
                    && assertEquals("Tester", p.getName(), "Player name")
                    && assertEquals(3, p.getLives(), "Default lives");
        } catch (Exception e) {
            return fail("Player initialization", e);
        }
    }

    private static boolean testPlayerAddExp() {
        try {
            Player p = new Player("Tester", 100);
            p.addExp(25);
            return assertEquals(125, p.getExp(), "Player add EXP");
        } catch (Exception e) {
            return fail("Player add EXP", e);
        }
    }

    private static boolean testPlayerAddItem() {
        try {
            Player p = new Player("Tester");
            Item coin = new Item("Coin", "A shiny gold coin");
            p.addItem(coin);
            return assertTrue(p.hasItem("Coin"), "Player has item");
        } catch (Exception e) {
            return fail("Player add item", e);
        }
    }

    private static boolean testDoorFactoryCreatesDoor() {
        try {
            DoorFactory df = new DoorFactory();
            Door d = df.createRandomDoor(1);
            return assertNotNull(d, "DoorFactory creates door");
        } catch (Exception e) {
            return fail("Door factory creates door", e);
        }
    }

    private static boolean testDoorInteractionReturnsResult() {
        try {
            Player p = new Player("Tester");
            DoorFactory df = new DoorFactory();
            Door d = df.createRandomDoor(1);
            String res = d.interact(p);
            return assertNotNull(res, "Door interaction returns result")
                    && assertTrue(res.length() > 0, "Result not empty");
        } catch (Exception e) {
            return fail("Door interaction", e);
        }
    }

    private static boolean testResourcesFileExists() {
        try {
            java.io.File f = new java.io.File("resources/doors.txt");
            return assertTrue(f.exists(), "doors.txt exists")
                    && assertTrue(f.length() > 0, "doors.txt not empty");
        } catch (Exception e) {
            return fail("Resources file exists", e);
        }
    }

    private static boolean testGameSingletonInstance() {
        try {
            Game g1 = Game.getInstance();
            Game g2 = Game.getInstance();
            return assertSame(g1, g2, "Game singleton same instance");
        } catch (Exception e) {
            return fail("Game singleton", e);
        }
    }

    private static boolean testPlayerLivesManagement() {
        try {
            Player p = new Player("TestPlayer");
            if (!assertEquals(3, p.getLives(), "Initial lives"))
                return false;
            p.loseLife();
            if (!assertEquals(2, p.getLives(), "Lives after 1 loss"))
                return false;
            p.loseLife();
            p.loseLife();
            p.loseLife();
            return assertEquals(0, p.getLives(), "Lives at 0");
        } catch (Exception e) {
            return fail("Player lives management", e);
        }
    }

    private static boolean testDiceSystemRoll() {
        try {
            DiceSystem ds = new DiceSystem();
            for (int i = 0; i < 100; i++) {
                int roll = ds.roll();
                if (!(roll >= 1 && roll <= 6)) {
                    System.out.println("  [FAIL] Dice roll out of range: " + roll);
                    return false;
                }
            }
            return true;
        } catch (Exception e) {
            return fail("Dice system roll", e);
        }
    }

    private static boolean testDiceSystemHPDetermination() {
        try {
            DiceSystem ds = new DiceSystem();
            return assertEquals(50, ds.getHPFromRoll(1), "Roll 1 HP")
                    && assertEquals(50, ds.getHPFromRoll(2), "Roll 2 HP")
                    && assertEquals(100, ds.getHPFromRoll(3), "Roll 3 HP")
                    && assertEquals(100, ds.getHPFromRoll(4), "Roll 4 HP")
                    && assertEquals(200, ds.getHPFromRoll(5), "Roll 5 HP")
                    && assertEquals(200, ds.getHPFromRoll(6), "Roll 6 HP");
        } catch (Exception e) {
            return fail("Dice HP determination", e);
        }
    }

    private static boolean testDoorFactoryVariety() {
        try {
            DoorFactory factory = new DoorFactory();
            Door door1 = factory.createRandomDoor(0);
            Door door2 = factory.createRandomDoor(1);
            return assertNotNull(door1, "Door 1 created")
                    && assertNotNull(door2, "Door 2 created");
        } catch (Exception e) {
            return fail("Door factory variety", e);
        }
    }

    private static boolean testPlayerExpPersistence() {
        try {
            Player p = new Player("TestPlayer");
            p.setExp(150);
            int before = p.getExp();
            p.loseLife();
            int after = p.getExp();
            return assertEquals(before, after, "EXP persists after life loss");
        } catch (Exception e) {
            return fail("EXP persistence", e);
        }
    }

    private static boolean testRewardDoorInteraction() {
        try {
            Player p = new Player("TestPlayer");
            RewardDoor door = new RewardDoor("Reward Door", "A shiny chest", 50);
            String result = door.interact(p);
            return assertNotNull(result, "Reward door result")
                    && assertTrue(result.length() > 0, "Result not empty");
        } catch (Exception e) {
            return fail("Reward door interaction", e);
        }
    }

    private static boolean testPenaltyDoorInteraction() {
        try {
            Player p = new Player("TestPlayer");
            PenaltyDoor door = new PenaltyDoor("Penalty Door", "A poison bottle", 25);
            String result = door.interact(p);
            return assertNotNull(result, "Penalty door result")
                    && assertTrue(result.length() > 0, "Result not empty");
        } catch (Exception e) {
            return fail("Penalty door interaction", e);
        }
    }

    private static boolean testMinigameDoorProperties() {
        try {
            MinigameDoor pongDoor = new MinigameDoor("Pong Door", "Table tennis", "PONG");
            return assertEquals("PONG", pongDoor.getGameType(), "Game type")
                    && assertEquals("Pong Door", pongDoor.getName(), "Name");
        } catch (Exception e) {
            return fail("Minigame door properties", e);
        }
    }

    private static boolean assertEquals(int expected, int actual, String message) {
        if (expected == actual) {
            return true;
        }
        System.out.println("  [FAIL] " + message + " - expected " + expected + ", got " + actual);
        return false;
    }

    private static boolean assertEquals(String expected, String actual, String message) {
        if (expected == null ? actual == null : expected.equals(actual)) {
            return true;
        }
        System.out.println("  [FAIL] " + message + " - expected '" + expected + "', got '" + actual + "'");
        return false;
    }

    private static boolean assertSame(Object expected, Object actual, String message) {
        if (expected == actual) {
            return true;
        }
        System.out.println("  [FAIL] " + message + " - objects not same");
        return false;
    }

    private static boolean assertNotNull(Object obj, String message) {
        if (obj != null) {
            return true;
        }
        System.out.println("  [FAIL] " + message + " - was null");
        return false;
    }

    private static boolean assertTrue(boolean condition, String message) {
        if (condition) {
            return true;
        }
        System.out.println("  [FAIL] " + message + " - was false");
        return false;
    }

    private static boolean fail(String message, Exception e) {
        System.out.println("  [FAIL] " + message + " - " + e.getMessage());
        return false;
    }
}