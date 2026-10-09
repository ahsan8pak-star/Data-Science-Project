// SoundManager Class - Central WAV Sound Manager for Space Mission
// Uses Multiple Path Resolution Strategies to Ensure Sounds Load Correctly
// Regardless of Working Directory - Fixes Pong and Minigame Sound Registration
// All Methods Are Try-Catch Wrapped to Prevent Audio Crashes
// Place WAV Files in: resources/Sound Effects/

import javax.sound.sampled.*;
import java.io.File;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class SoundManager {

    // Sound Effects Folder Name
    private static final String SOUND_FOLDER = "Sound Effects";

    // Active Looping Clips Tracked by Filename Key
    private static final Map<String, Clip> activeLoops = new HashMap<>();

    // Sound File Name Constants

    // Main Menu and Navigation
    public static final String MENU_NAVIGATE = "Movement 1.wav";
    public static final String MENU_SELECT = "Main Menu GUI.wav";
    public static final String TYPEWRITER = "Name Typped.wav";

    // Dialogue
    public static final String DIALOGUE_YES = "Yes Pressed.wav";
    public static final String DIALOGUE_NO = "No Pressed.wav";
    public static final String HORROR_LOOP = "Game Over - No Input.wav";

    // Door Selection
    public static final String DOOR_NAVIGATE = "Movement 2.wav";
    public static final String DOOR_OPEN = "Nothing Door Open.wav";
    public static final String DOOR_CLOSE = "Nothing Door Shut.wav";

    // Reward Door
    public static final String CHEST_SHINE = "Shiny Chest.wav";
    public static final String REWARD_POINTS = "EXP Gained.wav";

    // Penalty Door
    public static final String POISON_SMOKE = "Poison Bottle.wav";
    public static final String PENALTY_POINTS = "EXP Lost.wav";

    // Player Life Events
    public static final String LIFE_LOST = "Life Lost.wav";
    public static final String GAME_OVER_SOUND = "Game Over.wav";
    public static final String GAME_WIN_SOUND = "Game Won.wav";

    // Pong Minigame
    public static final String PONG_PLAYER_HIT = "Player Pong.wav";
    public static final String PONG_CPU_HIT = "CPU Pong.wav";
    public static final String PONG_PLAYER_POINT = "Player Point Pong.wav";
    public static final String PONG_CPU_POINT = "CPU Point.wav";
    public static final String PONG_WIN = "Pong Win.wav";
    public static final String PONG_LOSE = "Pong Lose.wav";

    // Space Invaders Minigame
    public static final String SI_PLAYER_SHOOT = "Player Shoot.wav";
    public static final String SI_MINI_LIFE_LOST = "Minilife lost.wav";
    public static final String SI_UFO_FLY = "UFO Hovering.wav";
    public static final String SI_UFO_SHOOT = "UFO Shooting.wav";
    public static final String SI_UFO_DIE = "UFO Crashing.wav";
    public static final String SI_SPACECRAFT_SHOOT = "Spacecraft Shooting.wav";
    public static final String SI_SPACECRAFT_DIE = "Spacecraft Crashed.wav";
    public static final String SI_ALIEN_SHOOT = "Aliens Shooting.wav";
    public static final String SI_ALIEN_DIE = "Alien Killed.wav";
    public static final String SI_NEXT_WAVE = "Point.wav";
    public static final String SI_WIN = "Space Invader Won.wav";
    public static final String SI_LOSE = "Game Lost.wav";

    // Resolve the Sound File Using Multiple Path Strategies
    // This Fixes Pong Sounds Not Registering Due to Working Directory Mismatch
    private static File resolveFile(String soundFile) {
        if (soundFile == null || soundFile.isBlank())
            return null;

        // Strategy 1: Relative from Current Working Directory
        String[] candidates = {
                "resources" + File.separator + SOUND_FOLDER + File.separator + soundFile,
                "resources/" + SOUND_FOLDER + "/" + soundFile,
                "../resources/" + SOUND_FOLDER + "/" + soundFile,
                "src/../resources/" + SOUND_FOLDER + "/" + soundFile,
        };

        for (String path : candidates) {
            File f = new File(path);
            if (f.exists() && f.isFile())
                return f;
        }

        // Strategy 2: Absolute Path from the JAR or Class Location
        try {
            String jarDir = SoundManager.class
                    .getProtectionDomain()
                    .getCodeSource()
                    .getLocation()
                    .toURI()
                    .getPath();
            File jarParent = new File(jarDir).getParentFile();

            String[] jarRelative = {
                    jarParent + File.separator + "resources" + File.separator + SOUND_FOLDER + File.separator
                            + soundFile,
                    jarParent + File.separator + ".." + File.separator + "resources" + File.separator + SOUND_FOLDER
                            + File.separator + soundFile,
                    jarParent + File.separator + ".." + File.separator + ".." + File.separator + "resources"
                            + File.separator + SOUND_FOLDER + File.separator + soundFile
            };

            for (String path : jarRelative) {
                File f = new File(path).getCanonicalFile();
                if (f.exists() && f.isFile())
                    return f;
            }
        } catch (Exception ignored) {
            // Path Resolution from JAR Failed - Continue to Next Strategy
        }

        // Strategy 3: Classpath Resource Stream Fallback
        try {
            URL url = SoundManager.class.getClassLoader()
                    .getResource("Sound Effects/" + soundFile);
            if (url != null)
                return new File(url.toURI());
        } catch (Exception ignored) {
            // Classpath Lookup Failed
        }

        return null;
    }

    // Apply Per-Sound Volume from SoundSettings to the Given Clip
    private static void applyVolume(Clip clip, String soundFile) {
        try {
            if (!clip.isControlSupported(FloatControl.Type.MASTER_GAIN))
                return;
            int vol = SoundSettings.getVolume(soundFile);
            FloatControl gain = (FloatControl) clip.getControl(FloatControl.Type.MASTER_GAIN);
            float dB;
            if (vol <= 0) {
                dB = gain.getMinimum();
            } else {
                dB = (float) (20.0 * Math.log10(vol / 100.0));
                dB = Math.max(gain.getMinimum(), Math.min(gain.getMaximum(), dB));
            }
            gain.setValue(dB);
        } catch (Exception ignored) {
            // Volume Control Not Supported on This System - Silently Skip
        }
    }

    // Update a Currently Looping Clip's Volume Without Restarting It
    public static void updateLoopVolume(String soundFile) {
        try {
            Clip clip = activeLoops.get(soundFile);
            if (clip != null && clip.isRunning()) {
                applyVolume(clip, soundFile);
            }
        } catch (Exception ignored) {
            // Live Volume Update Failed - Silently Skip
        }
    }

    // Play a WAV File Exactly Once
    // Silently Ignored if the File Cannot Be Found or the Audio Line Is Unavailable
    public static void playOnce(String soundFile) {
        if (soundFile == null || soundFile.isBlank())
            return;
        try {
            File file = resolveFile(soundFile);
            if (file == null)
                return;

            AudioInputStream stream = AudioSystem.getAudioInputStream(file);
            Clip clip = AudioSystem.getClip();
            clip.open(stream);
            applyVolume(clip, soundFile);

            clip.addLineListener(event -> {
                if (event.getType() == LineEvent.Type.STOP) {
                    try {
                        clip.close();
                    } catch (Exception ignored) {
                    }
                }
            });

            clip.start();

        } catch (UnsupportedAudioFileException ignored) {
            // Unsupported WAV Format - Skip
        } catch (LineUnavailableException ignored) {
            // Audio Line Busy - Skip
        } catch (Exception ignored) {
            // Any Other Error - Skip Silently
        }
    }

    // Play a WAV File in a Continuous Loop
    // Any Existing Loop for This Sound Is Stopped First
    public static void playLoop(String soundFile) {
        if (soundFile == null || soundFile.isBlank())
            return;
        try {
            stopSound(soundFile);

            File file = resolveFile(soundFile);
            if (file == null)
                return;

            AudioInputStream stream = AudioSystem.getAudioInputStream(file);
            Clip clip = AudioSystem.getClip();
            clip.open(stream);
            applyVolume(clip, soundFile);
            clip.loop(Clip.LOOP_CONTINUOUSLY);
            clip.start();

            activeLoops.put(soundFile, clip);

        } catch (UnsupportedAudioFileException ignored) {
            // Unsupported WAV Format - Skip
        } catch (LineUnavailableException ignored) {
            // Audio Line Busy - Skip
        } catch (Exception ignored) {
            // Any Other Error - Skip Silently
        }
    }

    // Stop a Specific Looping Sound by Its Filename Key
    public static void stopSound(String soundFile) {
        if (soundFile == null || soundFile.isBlank())
            return;
        try {
            Clip clip = activeLoops.remove(soundFile);
            if (clip != null) {
                try {
                    if (clip.isRunning())
                        clip.stop();
                    clip.close();
                } catch (Exception ignored) {
                }
            }
        } catch (Exception ignored) {
        }
    }

    // Stop All Currently Looping Sounds
    public static void stopAll() {
        try {
            for (Map.Entry<String, Clip> entry : activeLoops.entrySet()) {
                try {
                    Clip clip = entry.getValue();
                    if (clip != null) {
                        if (clip.isRunning())
                            clip.stop();
                        clip.close();
                    }
                } catch (Exception ignored) {
                }
            }
            activeLoops.clear();
        } catch (Exception ignored) {
        }
    }

    // Returns True if a Specific Loop Is Currently Active and Running
    public static boolean isLooping(String soundFile) {
        try {
            Clip clip = activeLoops.get(soundFile);
            return clip != null && clip.isRunning();
        } catch (Exception e) {
            return false;
        }
    }
}
