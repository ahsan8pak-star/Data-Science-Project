// OptionsScreen Class - Game Settings: Difficulty, Sound, Volume, Back
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
    private static final int OPT_SOUND = 1;
    private static final int OPT_VOLUME = 2;
    private static final int OPT_BACK = 3;

    private final String[] options = {
            "DIFFICULTY: NORMAL",
            "SOUND: ON",
            "VOLUME: 50",
            "BACK TO MAIN MENU"
    };

    private int selectedOption = 0;
    private int hoveredOption = -1;
    private boolean soundEnabled = true;
    private int volume = 50;

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
        switch (selectedOption) {
            // Cycle Backward (2 Forward = 1 Back for 3 States)
            case OPT_DIFFICULTY -> {
                GameSettings.cycleDifficulty();
                GameSettings.cycleDifficulty();
                refreshOptionTexts();
            }
            case OPT_SOUND -> {
                soundEnabled = !soundEnabled;
                refreshOptionTexts();
            }
            case OPT_VOLUME -> {
                volume = Math.max(0, volume - 1);
                refreshOptionTexts();
            }
        }
    }

    private void handleRight() {
        switch (selectedOption) {
            case OPT_DIFFICULTY -> {
                GameSettings.cycleDifficulty();
                refreshOptionTexts();
            }
            case OPT_SOUND -> {
                soundEnabled = !soundEnabled;
                refreshOptionTexts();
            }
            case OPT_VOLUME -> {
                volume = Math.min(100, volume + 1);
                refreshOptionTexts();
            }
        }
    }

    private void handleEnter() {
        switch (selectedOption) {
            case OPT_DIFFICULTY -> {
                GameSettings.cycleDifficulty();
                refreshOptionTexts();
            }
            case OPT_SOUND -> {
                soundEnabled = !soundEnabled;
                refreshOptionTexts();
            }
            case OPT_BACK -> controller.goBackToMainMenu();
        }
    }

    private void refreshOptionTexts() {
        options[OPT_DIFFICULTY] = "DIFFICULTY: " + GameSettings.difficultyLabel();
        options[OPT_SOUND] = "SOUND: " + (soundEnabled ? "ON" : "OFF");
        options[OPT_VOLUME] = "VOLUME: " + volume;
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

            // Volume Slider
            if (i == OPT_VOLUME) {
                int sW = 300, sH = 12, sX = W / 2 - sW / 2, sY = optY + 22;
                g2d.setColor(new Color(30, 30, 30, 200));
                g2d.fillRect(sX, sY, sW, sH);
                g2d.setColor(ACCENT_GREEN);
                g2d.fillRect(sX, sY, (int) (volume / 100.0 * sW), sH);
                g2d.setColor(new Color(0, 255, 0));
                g2d.drawRect(sX, sY, sW, sH);
            }

            optY += optSpc;
        }

        // Hints
        Font hint = new Font("Monospaced", Font.PLAIN, 13);
        g2d.setColor(new Color(0, 200, 0));
        drawCenteredText(g2d,
                "Use Up/Down or WASD to move, Left/Right or A/D to adjust volume (1 unit)",
                W / 2, H - 120, hint);
        drawCenteredText(g2d,
                "ENTER to toggle SOUND, ESC to go back, Mouse click to select",
                W / 2, H - 92, hint);
        drawCenteredText(g2d,
                "Difficulty affects Pong AI and Space Invaders speed / shooting",
                W / 2, H - 64, hint);
    }
}