// SoundSettings Class - Global Per-Sound Volume Storage with User-Friendly Display Names
// Volumes Are Stored as 0 to 100 Integers (100 = Full, 0 = Silent)
// Display Names Are Used in the Sound Settings Screen

import java.util.LinkedHashMap;
import java.util.Map;

public class SoundSettings {

    // Per-Sound Volume Map
    private static final Map<String, Integer> volumes = new LinkedHashMap<>();

    // User-Friendly Display Name Map
    private static final Map<String, String> displayNames = new LinkedHashMap<>();

    static {
        // Navigation Sounds
        reg(SoundManager.MENU_NAVIGATE, "Menu Navigation", 100);
        reg(SoundManager.MENU_SELECT, "Menu Confirm", 100);
        reg(SoundManager.TYPEWRITER, "Name Entry Key", 100);

        // Dialogue Sounds
        reg(SoundManager.DIALOGUE_YES, "Yes Choice", 100);
        reg(SoundManager.DIALOGUE_NO, "No Choice", 100);
        reg(SoundManager.HORROR_LOOP, "Rejection Music", 100);

        // Door Sounds
        reg(SoundManager.DOOR_NAVIGATE, "Door Switching", 100);
        reg(SoundManager.DOOR_OPEN, "Door Opening", 100);
        reg(SoundManager.DOOR_CLOSE, "Door Closing", 100);
        reg(SoundManager.CHEST_SHINE, "Chest Reveal", 100);
        reg(SoundManager.REWARD_POINTS, "EXP Gain Jingle", 100);
        reg(SoundManager.POISON_SMOKE, "Poison Reveal", 100);
        reg(SoundManager.PENALTY_POINTS, "EXP Loss Jingle", 100);

        // Player Life and End Game Sounds
        reg(SoundManager.LIFE_LOST, "Life Lost", 100);
        reg(SoundManager.GAME_OVER_SOUND, "Game Over Music", 100);
        reg(SoundManager.GAME_WIN_SOUND, "Victory Theme", 100);

        // Pong Minigame Sounds
        reg(SoundManager.PONG_PLAYER_HIT, "Pong Player Hit", 100);
        reg(SoundManager.PONG_CPU_HIT, "Pong CPU Hit", 100);
        reg(SoundManager.PONG_PLAYER_POINT, "Pong Player Point", 100);
        reg(SoundManager.PONG_CPU_POINT, "Pong CPU Point", 100);
        reg(SoundManager.PONG_WIN, "Pong Victory", 100);
        reg(SoundManager.PONG_LOSE, "Pong Defeat", 100);

        // Space Invaders Minigame Sounds
        reg(SoundManager.SI_PLAYER_SHOOT, "Invaders Player Shot", 100);
        reg(SoundManager.SI_MINI_LIFE_LOST, "Invaders Player Hit", 100);
        reg(SoundManager.SI_UFO_FLY, "Invaders UFO Engine Loop", 100);
        reg(SoundManager.SI_UFO_SHOOT, "Invaders UFO Fire", 100);
        reg(SoundManager.SI_UFO_DIE, "Invaders UFO Explosion", 100);
        reg(SoundManager.SI_SPACECRAFT_SHOOT, "Invaders Ship Fire", 100);
        reg(SoundManager.SI_SPACECRAFT_DIE, "Invaders Ship Explosion", 100);
        reg(SoundManager.SI_ALIEN_SHOOT, "Invaders Alien March Loop", 100);
        reg(SoundManager.SI_ALIEN_DIE, "Invaders Alien Kill", 100);
        reg(SoundManager.SI_NEXT_WAVE, "Invaders Wave Clear", 100);
        reg(SoundManager.SI_WIN, "Invaders Victory", 100);
        reg(SoundManager.SI_LOSE, "Invaders Defeat", 100);
    }

    // Register a Sound File with Its Display Name and Default Volume
    private static void reg(String file, String name, int vol) {
        displayNames.put(file, name);
        volumes.put(file, vol);
    }

    // Get the 0 to 100 Volume for the Given Sound File
    public static int getVolume(String soundFile) {
        return volumes.getOrDefault(soundFile, 100);
    }

    // Set the 0 to 100 Volume for the Given Sound File
    public static void setVolume(String soundFile, int vol) {
        volumes.put(soundFile, Math.max(0, Math.min(100, vol)));
        SoundManager.updateLoopVolume(soundFile);
    }

    // Get the User-Friendly Display Name for the Given Sound File
    public static String getDisplayName(String soundFile) {
        return displayNames.getOrDefault(soundFile, soundFile);
    }

    // Get All Registered Sound Files in Insertion Order
    public static String[] getAllSoundFiles() {
        return volumes.keySet().toArray(new String[0]);
    }

    // Get Sound Files Whose Display Name Starts with the Given Category Prefix
    public static String[] getSoundFilesForCategory(String categoryPrefix) {
        return volumes.keySet().stream()
                .filter(k -> displayNames.getOrDefault(k, "").startsWith(categoryPrefix))
                .toArray(String[]::new);
    }

    // Get Sound Files That Do Not Belong to a Minigame Category
    public static String[] getGeneralSoundFiles() {
        return volumes.keySet().stream()
                .filter(k -> {
                    String n = displayNames.getOrDefault(k, "");
                    return !n.startsWith("Pong") && !n.startsWith("Invaders");
                })
                .toArray(String[]::new);
    }
}