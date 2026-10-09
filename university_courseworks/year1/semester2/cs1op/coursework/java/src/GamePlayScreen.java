// GamePlayScreen Class - Main Gameplay Status Screen
// WIN: Plays GAME_WIN_SOUND Once
// DEAD and BANKRUPT: Loops GAME_OVER_SOUND Until ESC
// All Colors are Arcade Green on Black Background

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class GamePlayScreen extends BaseGameScreen {

    // Tracks the Last Sound State to Prevent Re-Firing on Every Repaint
    private String lastSoundState = "NONE";

    // Constructor
    public GamePlayScreen(GameGUI gui, GameController controller) {
        super(gui, controller);
        setupKeyListener();

        addComponentListener(new ComponentAdapter() {
            @Override
            public void componentShown(ComponentEvent e) {
                checkAndPlayStateSound();
            }
        });
    }

    // Determine Player State and Play the Appropriate Sound Once Per State Entry
    private void checkAndPlayStateSound() {
        try {
            Player player = controller.getCurrentPlayer();
            if (player == null)
                return;

            String currentState;
            if (player.getExp() >= 500) {
                currentState = "WIN";
            } else if (player.getLives() <= 0) {
                currentState = "DEAD";
            } else if (player.getExp() < 0) {
                currentState = "BANKRUPT";
            } else {
                lastSoundState = "NONE";
                return;
            }

            if (!currentState.equals(lastSoundState)) {
                lastSoundState = currentState;
                SoundManager.stopAll();

                switch (currentState) {
                    case "WIN" -> SoundManager.playOnce(SoundManager.GAME_WIN_SOUND);
                    case "DEAD", "BANKRUPT" -> SoundManager.playLoop(SoundManager.GAME_OVER_SOUND);
                }
            }
        } catch (Exception e) {
            // Silently Ignore Sound Errors
        }
    }

    // Keyboard Input Setup
    private void setupKeyListener() {
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                handleKeyPress(e.getKeyCode());
            }
        });
    }

    // Handle Key Presses Based on Current Player State
    private void handleKeyPress(int keyCode) {
        try {
            Player player = controller.getCurrentPlayer();
            if (player == null)
                return;

            if (player.getExp() >= 500) {
                if (keyCode == KeyEvent.VK_ENTER) {
                    SoundManager.stopAll();
                    controller.showScreen("DIALOGUE");
                } else if (keyCode == KeyEvent.VK_ESCAPE) {
                    SoundManager.stopAll();
                    controller.goBackToMainMenu();
                }
                return;
            }

            if (player.getLives() <= 0 || player.getExp() < 0) {
                if (keyCode == KeyEvent.VK_ESCAPE) {
                    SoundManager.stopSound(SoundManager.GAME_OVER_SOUND);
                    SoundManager.stopAll();
                    controller.goBackToMainMenu();
                }
                return;
            }

            if (keyCode == KeyEvent.VK_ESCAPE) {
                SoundManager.stopAll();
                controller.goBackToMainMenu();
            } else {
                lastSoundState = "NONE";
                controller.showScreen("DOOR_SELECTION");
            }

        } catch (Exception e) {
            // Silently Ignore Key Handler Errors
        }
    }

    // Render the Gameplay Status Screen
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        enableAntiAliasing(g2d);
        int width = getWidth();
        int height = getHeight();

        drawBorder(g2d, 50, 50, width - 100, height - 100, 2);

        g2d.setFont(new Font("Monospaced", Font.BOLD, 32));
        g2d.setColor(ARC_LIME);
        drawCenteredText(g2d, "SPACE MISSION", width / 2, 100, null);

        if (controller.getCurrentPlayer() != null) {
            Player player = controller.getCurrentPlayer();

            g2d.setColor(ARC_TEXT);
            g2d.setFont(new Font("Monospaced", Font.PLAIN, 18));
            g2d.drawString("Pilot: " + player.getName(), 80, 160);
            g2d.drawString("EXP Collected: " + player.getExp() + " / 500", 80, 200);
            g2d.drawString("Lives Remaining: " + player.getLives(), 80, 240);

            // Victory State
            if (player.getExp() >= 500) {
                g2d.setColor(ARC_LIME);
                g2d.setFont(new Font("Monospaced", Font.BOLD, 36));
                drawCenteredText(g2d, "MISSION ACCOMPLISHED!", width / 2, 320, null);
                g2d.setFont(new Font("Monospaced", Font.PLAIN, 20));
                g2d.setColor(ARC_TEXT);
                g2d.drawString("You Have Gathered Enough EXP to Return Home!", 80, 370);
                g2d.drawString("Congratulations, " + player.getName() + "!", 80, 400);
                g2d.setColor(ARC_DIM);
                g2d.setFont(new Font("Monospaced", Font.PLAIN, 14));
                drawCenteredText(g2d, "Press ENTER to Continue or ESC to Quit", width / 2, 460, null);

                // Lives Depleted State
            } else if (player.getLives() <= 0) {
                g2d.setColor(ARC_TEXT);
                g2d.setFont(new Font("Monospaced", Font.BOLD, 36));
                drawCenteredText(g2d, "YOU DIED", width / 2, 300, null);
                g2d.setFont(new Font("Monospaced", Font.PLAIN, 20));
                g2d.drawString("Your Journey Has Ended...", 80, 350);
                g2d.drawString("Final EXP: " + player.getExp(), 80, 385);
                g2d.setColor(ARC_DIM);
                g2d.setFont(new Font("Monospaced", Font.BOLD, 18));
                drawCenteredText(g2d, "Press ESC to Return to Menu", width / 2, 450, null);

                // EXP Depleted State
            } else if (player.getExp() < 0) {
                g2d.setColor(ARC_TEXT);
                g2d.setFont(new Font("Monospaced", Font.BOLD, 36));
                drawCenteredText(g2d, "GAME OVER", width / 2, 300, null);
                g2d.setFont(new Font("Monospaced", Font.PLAIN, 20));
                g2d.drawString("Your EXP Was Completely Depleted!", 80, 350);
                g2d.drawString("Final EXP: " + player.getExp(), 80, 385);
                g2d.drawString("The Void Has Claimed You...", 80, 420);
                g2d.setColor(ARC_DIM);
                g2d.setFont(new Font("Monospaced", Font.BOLD, 18));
                drawCenteredText(g2d, "Press ESC to Return to Menu", width / 2, 470, null);

                // Normal Gameplay
            } else {
                g2d.setColor(ARC_DIM);
                g2d.setFont(new Font("Monospaced", Font.PLAIN, 14));
                g2d.drawString("Navigate Doors to Gain Experience and Complete Your Mission!", 80, 360);
                g2d.drawString("Reward Doors Provide EXP, Penalty Doors Drain EXP,", 80, 400);
                g2d.drawString("and Minigame Doors Offer Challenging Opportunities.", 80, 430);
                g2d.setColor(ARC_NEON);
                g2d.setFont(new Font("Monospaced", Font.PLAIN, 16));
                drawCenteredText(g2d,
                        "Press Any Key to Enter the Next Round   |   ESC to Go Back to Menu",
                        width / 2, 500, null);
            }
        }
    }
}