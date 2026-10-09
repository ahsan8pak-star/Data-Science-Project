// NameEntryScreen Class - Player Name Input Screen
// Constraints: 1-15 Characters, Printable ASCII Only
// ESC to Go Back, ENTER to Confirm
// Sound: TYPEWRITER on Each Valid Character, MENU_SELECT on ENTER Confirm

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

public class NameEntryScreen extends BaseGameScreen {

    // Player Name Input Buffer
    private String playerName = "";

    // Maximum Permitted Name Length
    private static final int MAX_NAME_LENGTH = 15;

    // Constructor
    public NameEntryScreen(GameGUI gui, GameController controller) {
        super(gui, controller);
        setupKeyListener();
    }

    // Keyboard Input: Backspace, Printable Characters, ENTER, ESC
    private void setupKeyListener() {
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ESCAPE) {
                    SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                    controller.goBackToMainMenu();
                } else if (e.getKeyCode() == KeyEvent.VK_BACK_SPACE && !playerName.isEmpty()) {
                    playerName = playerName.substring(0, playerName.length() - 1);
                    SoundManager.playOnce(SoundManager.TYPEWRITER);
                    repaint();
                } else if (e.getKeyCode() == KeyEvent.VK_ENTER && !playerName.isEmpty()) {
                    SoundManager.playOnce(SoundManager.MENU_SELECT);
                    controller.setPlayerName(playerName);
                }
            }

            @Override
            public void keyTyped(KeyEvent e) {
                char c = e.getKeyChar();
                if (isValidCharacter(c) && playerName.length() < MAX_NAME_LENGTH) {
                    playerName += c;
                    SoundManager.playOnce(SoundManager.TYPEWRITER);
                    repaint();
                }
            }

            // Accept All Printable ASCII Characters
            private boolean isValidCharacter(char c) {
                return c >= ' ' && c <= '~';
            }
        });
    }

    // Render the Name Entry Screen
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        enableAntiAliasing(g2d);
        int width = getWidth();
        int height = getHeight();

        // Title in Lime Green
        Font titleFont = new Font("Monospaced", Font.BOLD, 56);
        g2d.setColor(ARC_LIME);
        drawCenteredText(g2d, "SPACE MISSION", width / 2, 120, titleFont);

        // Prompt Label
        Font labelFont = new Font("Monospaced", Font.BOLD, 32);
        g2d.setColor(ARC_NEON);
        drawCenteredText(g2d, "ENTER YOUR NAME", width / 2, 250, labelFont);

        // Input Box with Neon Border
        int boxX = 150;
        int boxY = 280;
        int boxWidth = width - 300;
        int boxHeight = 120;
        drawBorder(g2d, boxX, boxY, boxWidth, boxHeight, 3);

        // Input Text with Blinking Cursor Effect
        Font inputFont = new Font("Monospaced", Font.PLAIN, 28);
        g2d.setColor(ARC_TEXT);
        g2d.setFont(inputFont);
        g2d.drawString(playerName + "_", boxX + 40, boxY + 75);

        // Instructions at the Bottom
        Font infoFont = new Font("Monospaced", Font.PLAIN, 16);
        drawText(g2d,
                "Max " + MAX_NAME_LENGTH + " Characters   |   ENTER to Confirm",
                60, height - 100, infoFont, ARC_DIM);
        drawText(g2d,
                "Press ESC to Return to the Main Menu",
                60, height - 70, infoFont, ARC_DIM);
    }
}