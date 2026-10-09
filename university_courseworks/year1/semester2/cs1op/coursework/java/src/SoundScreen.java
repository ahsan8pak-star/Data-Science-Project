// SoundScreen Class - Individual Sound Volume Control Screen
// Accessible from the Main Menu via the SOUND Button
// Displays Every Sound File with a Friendly Title and a Draggable Volume Slider
// Sounds Are Grouped into Categories Switchable via Tabs

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.util.HashMap;
import java.util.Map;

public class SoundScreen extends BaseGameScreen {

    // Green Colour Palette
    private static final Color GREEN_BRIGHT = new Color(0, 255, 0);
    private static final Color GREEN_MID = new Color(0, 200, 0);
    private static final Color GREEN_DIM = new Color(0, 128, 0);
    private static final Color GREEN_DARK = new Color(0, 40, 0);

    // Category Tab Labels
    private static final String[] CATEGORIES = {
            "Navigation", "Dialogue", "Doors", "Player", "Pong", "Invaders"
    };

    // Sound Files Grouped by Category
    private static final String[][] CATEGORY_FILES = {
            // Navigation Sounds
            {
                    SoundManager.MENU_NAVIGATE,
                    SoundManager.MENU_SELECT,
                    SoundManager.TYPEWRITER
            },
            // Dialogue Sounds
            {
                    SoundManager.DIALOGUE_YES,
                    SoundManager.DIALOGUE_NO,
                    SoundManager.HORROR_LOOP
            },
            // Door Sounds
            {
                    SoundManager.DOOR_NAVIGATE,
                    SoundManager.DOOR_OPEN,
                    SoundManager.DOOR_CLOSE,
                    SoundManager.CHEST_SHINE,
                    SoundManager.REWARD_POINTS,
                    SoundManager.POISON_SMOKE,
                    SoundManager.PENALTY_POINTS
            },
            // Player Life and End Game Sounds
            {
                    SoundManager.LIFE_LOST,
                    SoundManager.GAME_OVER_SOUND,
                    SoundManager.GAME_WIN_SOUND
            },
            // Pong Minigame Sounds
            {
                    SoundManager.PONG_PLAYER_HIT,
                    SoundManager.PONG_CPU_HIT,
                    SoundManager.PONG_PLAYER_POINT,
                    SoundManager.PONG_CPU_POINT,
                    SoundManager.PONG_WIN,
                    SoundManager.PONG_LOSE
            },
            // Space Invaders Minigame Sounds
            {
                    SoundManager.SI_PLAYER_SHOOT,
                    SoundManager.SI_MINI_LIFE_LOST,
                    SoundManager.SI_UFO_FLY,
                    SoundManager.SI_UFO_SHOOT,
                    SoundManager.SI_UFO_DIE,
                    SoundManager.SI_SPACECRAFT_SHOOT,
                    SoundManager.SI_SPACECRAFT_DIE,
                    SoundManager.SI_ALIEN_SHOOT,
                    SoundManager.SI_ALIEN_DIE,
                    SoundManager.SI_NEXT_WAVE,
                    SoundManager.SI_WIN,
                    SoundManager.SI_LOSE
            }
    };

    // Currently Selected Category Tab Index
    private int selectedCategory = 0;

    // Slider Rectangles for Mouse Hit Testing
    private final HashMap<String, Rectangle> sliderRects = new HashMap<>();

    // Currently Dragged Slider Key
    private String draggingSlider = null;

    // Constructor
    public SoundScreen(GameGUI gui, GameController controller) {
        super(gui, controller);
        setupKeyListener();
        setupMouseListeners();
    }

    // Keyboard Navigation - Left/Right Switches Categories, ESC Returns to Menu
    private void setupKeyListener() {
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                switch (e.getKeyCode()) {
                    case KeyEvent.VK_ESCAPE -> {
                        SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                        controller.goBackToMainMenu();
                    }
                    case KeyEvent.VK_LEFT, KeyEvent.VK_A -> {
                        selectedCategory = Math.max(0, selectedCategory - 1);
                        SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                        repaint();
                    }
                    case KeyEvent.VK_RIGHT, KeyEvent.VK_D -> {
                        selectedCategory = Math.min(CATEGORIES.length - 1, selectedCategory + 1);
                        SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                        repaint();
                    }
                }
            }
        });
    }

    // Mouse Listeners for Clicking Tabs and Dragging Volume Sliders
    private void setupMouseListeners() {
        addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                handleMousePress(e.getPoint());
            }

            @Override
            public void mouseReleased(MouseEvent e) {
                draggingSlider = null;
            }
        });

        addMouseMotionListener(new MouseMotionAdapter() {
            @Override
            public void mouseDragged(MouseEvent e) {
                if (draggingSlider == null)
                    return;
                Rectangle r = sliderRects.get(draggingSlider);
                if (r == null)
                    return;
                int vol = (int) (100.0 * (e.getX() - r.x) / r.width);
                SoundSettings.setVolume(draggingSlider, vol);
                repaint();
            }
        });
    }

    // Handle Mouse Press Events for Tab Switching and Slider Dragging
    private void handleMousePress(java.awt.Point p) {
        int W = getWidth();
        int tabAreaW = W - 40;
        int tabW = tabAreaW / CATEGORIES.length;

        for (int i = 0; i < CATEGORIES.length; i++) {
            Rectangle tabRect = new Rectangle(20 + i * tabW, 80, tabW, 36);
            if (tabRect.contains(p)) {
                selectedCategory = i;
                SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                repaint();
                return;
            }
        }

        for (Map.Entry<String, Rectangle> entry : sliderRects.entrySet()) {
            if (entry.getValue().contains(p)) {
                draggingSlider = entry.getKey();
                int vol = (int) (100.0 * (p.x - entry.getValue().x) / entry.getValue().width);
                SoundSettings.setVolume(draggingSlider, vol);
                repaint();
                return;
            }
        }
    }

    // Render the Sound Settings Screen
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        enableAntiAliasing(g2d);
        int W = getWidth(), H = getHeight();

        drawBorder(g2d, 20, 20, W - 40, H - 40, 2);

        g2d.setFont(new Font("Monospaced", Font.BOLD, 32));
        g2d.setColor(GREEN_BRIGHT);
        drawCenteredText(g2d, "SOUND SETTINGS", W / 2, 65, null);

        // Category Tabs
        int tabAreaW = W - 40;
        int tabW = tabAreaW / CATEGORIES.length;

        for (int i = 0; i < CATEGORIES.length; i++) {
            int tx = 20 + i * tabW;
            boolean sel = (i == selectedCategory);

            g2d.setColor(sel ? GREEN_DIM : GREEN_DARK);
            g2d.fillRect(tx, 80, tabW, 36);

            g2d.setColor(GREEN_BRIGHT);
            g2d.setStroke(new BasicStroke(1));
            g2d.drawRect(tx, 80, tabW, 36);

            g2d.setFont(new Font("Monospaced", Font.BOLD, 13));
            FontMetrics fm = g2d.getFontMetrics();
            g2d.setColor(sel ? GREEN_BRIGHT : GREEN_MID);
            g2d.drawString(
                    CATEGORIES[i],
                    tx + (tabW - fm.stringWidth(CATEGORIES[i])) / 2,
                    103);
        }

        // Sound Sliders for the Active Category
        sliderRects.clear();
        String[] files = CATEGORY_FILES[selectedCategory];
        int labelX = 35;
        int sliderX = W / 3;
        int sliderW = (int) (W * 0.45);
        int volX = sliderX + sliderW + 12;
        int rowH = Math.min(42, (H - 160) / Math.max(1, files.length));
        int startY = 135;

        for (String file : files) {
            String displayName = SoundSettings.getDisplayName(file);
            int vol = SoundSettings.getVolume(file);

            // Sound Label
            g2d.setFont(new Font("Monospaced", Font.BOLD, 14));
            g2d.setColor(GREEN_BRIGHT);
            g2d.drawString(displayName, labelX, startY + rowH / 2 + 5);

            // Slider Track and Fill
            int sy = startY + rowH / 2 - 9;
            int sh = 18;
            Rectangle sliderRect = new Rectangle(sliderX, sy, sliderW, sh);
            sliderRects.put(file, sliderRect);

            g2d.setColor(new Color(0, 20, 0));
            g2d.fillRect(sliderRect.x, sliderRect.y, sliderRect.width, sliderRect.height);

            g2d.setColor(GREEN_MID);
            g2d.fillRect(sliderRect.x, sliderRect.y, (int) (sliderRect.width * vol / 100.0), sliderRect.height);

            g2d.setColor(GREEN_BRIGHT);
            g2d.setStroke(new BasicStroke(1));
            g2d.drawRect(sliderRect.x, sliderRect.y, sliderRect.width, sliderRect.height);

            // Slider Thumb
            int thumbX = sliderRect.x + (int) (sliderRect.width * vol / 100.0) - 4;
            g2d.fillRect(thumbX, sliderRect.y - 3, 8, sliderRect.height + 6);

            // Volume Percentage Label
            g2d.setFont(new Font("Monospaced", Font.PLAIN, 13));
            g2d.setColor(GREEN_MID);
            g2d.drawString(vol + "%", volX, startY + rowH / 2 + 5);

            startY += rowH;
        }

        // Bottom Hint Bar
        g2d.setFont(new Font("Monospaced", Font.PLAIN, 13));
        g2d.setColor(GREEN_DIM);
        drawCenteredText(
                g2d,
                "A / D or Left / Right to Switch Tab   |   Drag Sliders to Adjust Volume   |   ESC to Go Back",
                W / 2, H - 28, null);
    }
}