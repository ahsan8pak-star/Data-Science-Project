// MainMenuScreen Class - Main Menu with Title and Navigation Options
// Options: START GAME, SOUND, OPTIONS, QUIT
// Navigation: Arrow Keys, WASD, Mouse Hover, ENTER to Confirm
// Sound: MENU_NAVIGATE on Up/Down, MENU_SELECT on ENTER or Click

import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;

public class MainMenuScreen extends BaseGameScreen {

    // Menu Option Labels
    private final String[] options = { "START GAME", "SOUND", "OPTIONS", "QUIT" };

    // Keyboard Selected Option Index
    private int selectedOption = 0;

    // Mouse Hovered Option Index
    private int hoveredOption = -1;

    // Constructor
    public MainMenuScreen(GameGUI gui, GameController controller) {
        super(gui, controller);
        setupKeyListener();
        setupMouseListener();
    }

    // Setup Keyboard Navigation for Up/Down/Enter
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
                    case KeyEvent.VK_ENTER -> {
                        SoundManager.playOnce(SoundManager.MENU_SELECT);
                        handleSelection();
                    }
                }
            }
        });
    }

    // Setup Mouse Hover and Click Navigation
    private void setupMouseListener() {
        addMouseMotionListener(new MouseMotionAdapter() {
            @Override
            public void mouseMoved(MouseEvent e) {
                int mouseY = e.getY();
                int optionY = 330;
                int optSpacing = 85;
                int prevHovered = hoveredOption;
                hoveredOption = -1;

                for (int i = 0; i < options.length; i++) {
                    if (mouseY >= optionY - 25 && mouseY <= optionY + 25) {
                        hoveredOption = i;
                        break;
                    }
                    optionY += optSpacing;
                }

                if (hoveredOption != prevHovered && hoveredOption >= 0) {
                    SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                }
                repaint();
            }
        });

        addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (hoveredOption >= 0) {
                    selectedOption = hoveredOption;
                    SoundManager.playOnce(SoundManager.MENU_SELECT);
                    handleSelection();
                }
            }
        });
    }

    // Execute the Currently Selected Menu Option
    private void handleSelection() {
        switch (selectedOption) {
            case 0 -> controller.startGame();
            case 1 -> controller.showSoundScreen();
            case 2 -> controller.showOptions();
            case 3 -> {
                SoundManager.stopAll();
                System.exit(0);
            }
        }
    }

    // Render the Main Menu Screen
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        enableAntiAliasing(g2d);
        int width = getWidth();
        int height = getHeight();

        drawBorder(g2d, 50, 50, width - 100, height - 100, 3);

        // Title - Lime Green for Maximum Arcade Impact
        Font titleFont = new Font("Monospaced", Font.BOLD, 56);
        g2d.setColor(ARC_LIME);
        drawCenteredText(g2d, "SPACE MISSION", width / 2, 150, titleFont);

        // Subtitle Line in Dim Green
        g2d.setFont(new Font("Monospaced", Font.PLAIN, 14));
        g2d.setColor(ARC_DIM);
        drawCenteredText(g2d, "INSERT COIN TO CONTINUE", width / 2, 185, null);

        // Menu Options
        Font optionFont = new Font("Monospaced", Font.BOLD, 28);
        int optionY = 330;
        int optSpacing = 85;

        for (int i = 0; i < options.length; i++) {
            boolean isSelected = (i == selectedOption);
            boolean isHovered = (i == hoveredOption);

            if (isSelected || isHovered) {
                // Translucent Glow Behind the Selected Option
                g2d.setColor(ARC_GLOW);
                g2d.fillRect(width / 2 - 190, optionY - 26, 380, 52);
                // Neon Border Around the Selection
                g2d.setColor(ARC_NEON);
                g2d.drawRect(width / 2 - 190, optionY - 26, 380, 52);
                // Lime Text for Selected
                g2d.setColor(ARC_LIME);
                drawCenteredText(g2d, options[i], width / 2, optionY, optionFont);
            } else {
                g2d.setColor(ARC_TEXT);
                drawCenteredText(g2d, options[i], width / 2, optionY, optionFont);
            }

            optionY += optSpacing;
        }

        // Navigation Hint at the Bottom in Dim Green
        Font infoFont = new Font("Monospaced", Font.PLAIN, 14);
        drawText(
                g2d,
                "Up/Down  WASD  Mouse to Navigate   |   ENTER or Click to Select",
                60, height - 60, infoFont, ARC_DIM);
    }
}