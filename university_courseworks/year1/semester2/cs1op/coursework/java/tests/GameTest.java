// GameTest class - basic functionality tests

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class GameTest {
    
    // Test player initialization with EXP
    @Test
    public void testPlayerInitializationWithExp() {
        Player p = new Player("Tester", 100);
        assertEquals(100, p.getExp());
    }

    // Test adding EXP
    @Test
    public void testPlayerAddExp() {
        Player p = new Player("Tester", 100);
        p.addExp(25);
        assertEquals(125, p.getExp());
    }

    // Test adding item to inventory
    @Test
    public void testPlayerAddItem() {
        Player p = new Player("Tester");
        Item coin = new Item("Coin", "A shiny gold coin");
        p.addItem(coin);
        assertTrue(p.hasItem("Coin"));
    }

    // Test door factory creates doors
    @Test
    public void testDoorFactoryCreatesDoor() {
        DoorFactory df = new DoorFactory();
        Door d = df.createRandomDoor(1);
        assertNotNull(d, "DoorFactory should create a door");
    }

    // Test door interaction returns result

    @Test
    public void testDoorInteractionReturnsResult() {
        Player p = new Player("Tester");
        DoorFactory df = new DoorFactory();
        Door d = df.createRandomDoor(1);
        assertNotNull(d, "Door should be created");
        String res = d.interact(p);
        assertNotNull(res);
        assertTrue(res.length() > 0);
    }

    // Test resources file exists
    @Test
    public void testResourcesFileExists() {
        java.io.File f = new java.io.File("resources/doors.txt");
        assertTrue(f.exists(), "doors.txt should exist at resources/");
        assertTrue(f.length() > 0);
    }
}
