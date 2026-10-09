// DoorFactory - Factory Pattern
// Creates Door Instances from doors.txt or fallback

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class DoorFactory {

    private final Random rnd = new Random();
    private final List<String[]> templates = new ArrayList<>();

    public DoorFactory() {
        loadTemplates();
    }

    // Only Reads Lines that Starts with a Recognised Type Keyword
    private void loadTemplates() {
        File f = new File("resources/doors.txt");
        if (!f.exists())
            return;
        try (BufferedReader br = new BufferedReader(new FileReader(f))) {
            String line;
            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (line.isEmpty() || line.startsWith("#"))
                    continue;
                String[] parts = line.split("\\|");
                if (parts.length < 2)
                    continue;
                String type = parts[0].trim().toLowerCase();
                if (type.equals("reward") || type.equals("penalty") || type.equals("nothing")
                        || type.equals("pong minigame") || type.equals("space invaders minigame")
                        || type.equals("minigame")) {
                    templates.add(parts);
                }
            }
        } catch (IOException ignored) {
        }
    }

    public Door createRandomDoor(int index) {
        if (!templates.isEmpty()) {
            String[] parts = templates.get(rnd.nextInt(templates.size()));
            String type = parts[0].trim().toLowerCase();
            String desc = parts.length > 1 ? parts[1].trim() : "";
            int valIdx = 3; // format: Type | Description | ASCII_KEY | Value | Dice #

            return switch (type) {
                case "reward" -> {
                    int val = 50;
                    if (parts.length > valIdx) {
                        try {
                            val = Integer.parseInt(parts[valIdx].trim());
                        } catch (NumberFormatException ignored) {
                        }
                    }
                    yield new RewardDoor("Door " + index, desc, val);
                }
                case "penalty" -> {
                    int val = 25;
                    if (parts.length > valIdx) {
                        try {
                            val = Math.abs(Integer.parseInt(parts[valIdx].trim()));
                        } catch (NumberFormatException ignored) {
                        }
                    }
                    yield new PenaltyDoor("Door " + index, desc, val);
                }
                case "pong minigame" -> new MinigameDoor("Door " + index, desc, "PONG");
                case "space invaders minigame" -> new MinigameDoor("Door " + index, desc, "SPACE_INVADERS");
                case "nothing" -> new NothingDoor("Door " + index, desc);
                default -> createFallbackDoor(index);
            };
        }
        return createFallbackDoor(index);
    }

    private Door createFallbackDoor(int index) {
        int roll = rnd.nextInt(12);
        if (roll == 0)
            return new MinigameDoor("Mysterious Hatch", "A hatch to a strange craft.", "PONG");
        if (roll == 1)
            return new MinigameDoor("Strange Spacecraft", "A hatch into the unknown.", "SPACE_INVADERS");
        if (roll <= 4)
            return new PenaltyDoor("Trap Door", "A dark trap that drains energy.", 25 + rnd.nextInt(25));
        if (roll == 5)
            return new NothingDoor("Empty Door", "A door with nothing behind it.");
        return new RewardDoor("Safe Door", "A door that seems harmless.", 25 + rnd.nextInt(25));
    }
}