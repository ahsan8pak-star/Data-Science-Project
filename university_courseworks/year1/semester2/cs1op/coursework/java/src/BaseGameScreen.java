// BaseGameScreen Class - Abstract Base for All Game Screens
// Defines the Shared Arcade Color Palette Inspired by Space Invaders
// All Screen Classes Extend This to Inherit the Common Visual Style

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import javax.swing.JPanel;

public abstract class BaseGameScreen extends JPanel {

    // Reference to the Main Game Window
    protected GameGUI gui;

    // Reference to the Game Logic Controller
    protected GameController controller;

    // Arcade Color Palette - Six Distinct Green Variants
    // Inspired by the Classic Space Invaders Green-on-Black CRT Aesthetic

    // Neon Green - Used for Titles, Active Selection, and Primary Borders
    // Matches the Player Ship Color in the Original Space Invaders
    protected static final Color ARC_NEON = new Color(0, 255, 65);

    // Lime Green - Used for Highlighted Text and Glow Effects
    // Inspired by the Shield Barrier Color in Arcade Space Invaders
    protected static final Color ARC_LIME = new Color(100, 255, 60);

    // Standard Text Green - Used for Normal Body Text and Labels
    protected static final Color ARC_TEXT = new Color(0, 215, 0);

    // Dim Green - Used for Hints, Secondary Text, and Navigation Prompts
    protected static final Color ARC_DIM = new Color(0, 145, 0);

    // Panel Green - Used for Box Fills, Menu Backgrounds, and Dark Panels
    protected static final Color ARC_PANEL = new Color(0, 45, 0);

    // Glow Green - Semi-Transparent Overlay for the Door Selection Highlight
    // Alpha 70 Creates a Translucent Green Highlighter Effect
    protected static final Color ARC_GLOW = new Color(0, 200, 0, 70);

    // Background - Pure Black Matching the Arcade CRT Screen
    protected static final Color ARC_BG = Color.BLACK;

    // Legacy Aliases - Kept for Compatibility with Existing Code
    protected static final Color ACCENT_GREEN = ARC_NEON;
    protected static final Color BG_BLACK = ARC_BG;
    protected static final Color DARK_GREEN = ARC_PANEL;

    // Constructor - Sets Up the Black Background and Focus
    public BaseGameScreen(GameGUI gui, GameController controller) {
        this.gui = gui;
        this.controller = controller;
        setBackground(ARC_BG);
        setFocusable(true);
    }

    // Draw a Rectangular Border Using the Neon Green Arcade Color
    protected void drawBorder(Graphics2D g, int x, int y, int width, int height, int thickness) {
        g.setColor(ARC_NEON);
        g.setStroke(new BasicStroke(thickness));
        g.drawRect(x, y, width, height);
        g.setStroke(new BasicStroke(1));
    }

    // Draw a String Centred Horizontally Around the Given X Position
    protected void drawCenteredText(Graphics2D g, String text, int x, int y, Font font) {
        if (font != null)
            g.setFont(font);
        g.setColor(ARC_NEON);
        FontMetrics fm = g.getFontMetrics();
        g.drawString(text, x - fm.stringWidth(text) / 2, y);
    }

    // Draw a String at the Given Position with an Optional Font and Colour
    protected void drawText(Graphics2D g, String text, int x, int y, Font font, Color color) {
        if (font != null)
            g.setFont(font);
        g.setColor(color != null ? color : ARC_NEON);
        g.drawString(text, x, y);
    }

    // Enable Anti-Aliasing for Smoother Text and Shape Rendering
    protected void enableAntiAliasing(Graphics2D g2d) {
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
    }
}