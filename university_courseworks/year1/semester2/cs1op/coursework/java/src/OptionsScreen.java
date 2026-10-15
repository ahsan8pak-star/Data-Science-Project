// OptionsScreen Class - Game Settings: Difficulty, Display, Sound, Back
// Sound: MENU_NAVIGATE on Up/Down/Mouse Hover Change, MENU_SELECT on ENTER / Back

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class OptionsScreen extends BaseGameScreen {

    // Option Indices
    private static final int OPT_DIFFICULTY = 0;
    private static final int OPT_DISPLAY = 1;
    private static final int OPT_SOUND = 2;
    private static final int OPT_BACK = 3;

    private final String[] options = {
            "DIFFICULTY: NORMAL",
            "DISPLAY (CRT: OFF)",
            "SOUND SETTINGS",
            "BACK TO MAIN MENU"
    };

    private int selectedOption = 0;
    private int hoveredOption = -1;

    public OptionsScreen(GameGUI gui, GameController controller) {
        super(gui, controller);
        refreshOptionTexts();
        setupKeyListener();
        setupMouseListener();
    }

    // Key Navigation
    private void setupKeyListener() {
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                switch (e.getKeyCode()) {
                    case KeyEvent.VK_UP, KeyEvent.VK_W -> {
                        selectedOption = (selectedOption - 1 + options.length) % options.length;
                        SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                        repaint();
                    }
                    case KeyEvent.VK_DOWN, KeyEvent.VK_S -> {
                        selectedOption = (selectedOption + 1) % options.length;
                        SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                        repaint();
                    }
                    case KeyEvent.VK_LEFT, KeyEvent.VK_A -> {
                        handleLeft();
                        SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                        repaint();
                    }
                    case KeyEvent.VK_RIGHT, KeyEvent.VK_D -> {
                        handleRight();
                        SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                        repaint();
                    }
                    case KeyEvent.VK_ENTER -> {
                        SoundManager.playOnce(SoundManager.MENU_SELECT);
                        handleEnter();
                        repaint();
                    }
                    case KeyEvent.VK_ESCAPE -> {
                        SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                        controller.goBackToMainMenu();
                    }
                }
            }
        });
    }

    // Mouse Navigation
    private void setupMouseListener() {
        addMouseMotionListener(new java.awt.event.MouseMotionAdapter() {
            @Override
            public void mouseMoved(java.awt.event.MouseEvent e) {
                int mouseY = e.getY();
                int optY = 230;
                int optSpc = 95;
                int prevHovered = hoveredOption;
                hoveredOption = -1;
                for (int i = 0; i < options.length; i++) {
                    if (mouseY >= optY - 28 && mouseY <= optY + 28) {
                        hoveredOption = i;
                        break;
                    }
                    optY += optSpc;
                }
                // Play Navigate Sound Only When Hover Changes to a New Option
                if (hoveredOption != prevHovered && hoveredOption >= 0) {
                    SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                }
                repaint();
            }
        });
        addMouseListener(new java.awt.event.MouseAdapter() {
            @Override
            public void mouseClicked(java.awt.event.MouseEvent e) {
                if (hoveredOption >= 0) {
                    selectedOption = hoveredOption;
                    SoundManager.playOnce(SoundManager.MENU_SELECT);
                    handleEnter();
                    repaint();
                }
            }
        });
    }

    // Actions
    private void handleLeft() {
        if (selectedOption == OPT_DIFFICULTY) {
            // Cycle Backward (2 Forward = 1 Back for 3 States)
            GameSettings.cycleDifficulty();
            GameSettings.cycleDifficulty();
            refreshOptionTexts();
        }
    }

    private void handleRight() {
        if (selectedOption == OPT_DIFFICULTY) {
            GameSettings.cycleDifficulty();
            refreshOptionTexts();
        }
    }

    private void handleEnter() {
        switch (selectedOption) {
            case OPT_DIFFICULTY -> {
                GameSettings.cycleDifficulty();
                refreshOptionTexts();
            }
            case OPT_DISPLAY -> controller.showCRTScreen();
            case OPT_SOUND -> controller.showSoundScreen();
            case OPT_BACK -> controller.goBackToMainMenu();
        }
    }

    private void refreshOptionTexts() {
        options[OPT_DIFFICULTY] = "DIFFICULTY: " + GameSettings.difficultyLabel();
        options[OPT_DISPLAY] = "DISPLAY (CRT: " + (CRTSettings.isEnabled() ? "ON" : "OFF") + ")";
        // OPT_SOUND and OPT_BACK are static strings, no refresh needed
    }

    // Paint
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        enableAntiAliasing(g2d);
        int W = getWidth(), H = getHeight();

        drawBorder(g2d, 50, 50, W - 100, H - 100, 3);

        // Title
        g2d.setFont(new Font("Monospaced", Font.BOLD, 46));
        drawCenteredText(g2d, "OPTIONS", W / 2, 130, null);

        // Options
        Font optFont = new Font("Monospaced", Font.BOLD, 22);
        int optY = 230, optSpc = 95;

        for (int i = 0; i < options.length; i++) {
            boolean sel = (i == selectedOption) || (i == hoveredOption);
            if (sel) {
                g2d.setColor(DARK_GREEN);
                g2d.fillRect(W / 2 - 220, optY - 28, 440, 56);
                g2d.setColor(new Color(255, 255, 0));
            } else {
                g2d.setColor(ACCENT_GREEN);
            }
            drawCenteredText(g2d, options[i], W / 2, optY, optFont);
            optY += optSpc;
        }

        // Hints
        Font hint = new Font("Monospaced", Font.PLAIN, 13);
        g2d.setColor(new Color(0, 200, 0));
        drawCenteredText(g2d,
                "Use Up/Down or WASD to move, Left/Right or A/D to change difficulty",
                W / 2, H - 120, hint);
        drawCenteredText(g2d,
                "ENTER opens DISPLAY or SOUND, ESC returns to the main menu",
                W / 2, H - 92, hint);
        drawCenteredText(g2d,
                "Difficulty affects Pong AI and Space Invaders speed / shooting",
                W / 2, H - 64, hint);
    }
}
