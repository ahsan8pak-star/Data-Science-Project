// CRTScreen Class - Full-Screen CRT Display Settings Page
//
// This screen has no Java counterpart file: GameController builds a
// CRTScreen that does not exist in the Java sources, so the Java tree
// does not compile as committed. This implementation provides the
// clearly intended screen, reusing the pause-menu CRT semantics:
// an on/off toggle and a 0-100 intensity slider with the
// 0-33 / 34-66 / 67-100 band legend. ESC returns to options.

import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;

public class CRTScreen extends BaseGameScreen {

    // Whether the intensity slider (true) or the toggle (false) has focus
    private boolean focusIntensity = false;

    // Toggle button rectangles, set during paintComponent
    private int[] onRect;
    private int[] offRect;

    // Intensity slider rectangle, set during paintComponent
    private int[] sliderRect;

    public CRTScreen(GameGUI gui, GameController controller) {
        super(gui, controller);
        setupKeyListener();
        setupMouseListener();
    }

    // Key Navigation
    private void setupKeyListener() {
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                switch (e.getKeyCode()) {
                    case KeyEvent.VK_ESCAPE -> {
                        SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                        controller.showOptions();
                    }
                    case KeyEvent.VK_UP, KeyEvent.VK_W, KeyEvent.VK_DOWN, KeyEvent.VK_S -> {
                        focusIntensity = !focusIntensity;
                        SoundManager.playOnce(SoundManager.MENU_NAVIGATE);
                        repaint();
                    }
                    case KeyEvent.VK_LEFT, KeyEvent.VK_A -> {
                        if (focusIntensity) {
                            CRTSettings.setIntensity(CRTSettings.getIntensity() - 1);
                        } else {
                            CRTSettings.setEnabled(false);
                        }
                        repaint();
                    }
                    case KeyEvent.VK_RIGHT, KeyEvent.VK_D -> {
                        if (focusIntensity) {
                            CRTSettings.setIntensity(CRTSettings.getIntensity() + 1);
                        } else {
                            CRTSettings.setEnabled(true);
                        }
                        repaint();
                    }
                    case KeyEvent.VK_ENTER -> {
                        if (focusIntensity) {
                            if (CRTSettings.isEnabled()) {
                                CRTSettings.setEnabled(false);
                            } else {
                                CRTSettings.setEnabled(true);
                            }
                        } else {
                            SoundManager.playOnce(SoundManager.MENU_SELECT);
                            controller.showOptions();
                        }
                        repaint();
                    }
                }
            }
        });
    }

    // Mouse Navigation
    private void setupMouseListener() {
        addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                if (onRect != null && inside(e, onRect)) {
                    CRTSettings.setEnabled(true);
                    repaint();
                } else if (offRect != null && inside(e, offRect)) {
                    CRTSettings.setEnabled(false);
                    repaint();
                } else if (sliderRect != null && inside(e, sliderRect)) {
                    setIntensityFromMouse(e.getX());
                    repaint();
                }
            }
        });

        addMouseMotionListener(new MouseMotionAdapter() {
            @Override
            public void mouseDragged(MouseEvent e) {
                if (sliderRect != null) {
                    setIntensityFromMouse(e.getX());
                    repaint();
                }
            }
        });
    }

    // Set intensity from a mouse x position over the slider
    private void setIntensityFromMouse(int mouseX) {
        int x = sliderRect[0];
        int w = sliderRect[2];
        CRTSettings.setIntensity((int) (100.0 * (mouseX - x) / w));
    }

    // Check if a mouse event is inside a rectangle
    private boolean inside(MouseEvent e, int[] rect) {
        return e.getX() >= rect[0] && e.getX() <= rect[0] + rect[2]
                && e.getY() >= rect[1] && e.getY() <= rect[1] + rect[3];
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
        drawCenteredText(g2d, "CRT DISPLAY", W / 2, 130, null);

        // Toggle buttons
        boolean enabled = CRTSettings.isEnabled();
        int x = W / 2 - 120, y = 220;
        onRect = new int[]{x, y, 100, 40};
        offRect = new int[]{x + 130, y, 100, 40};

        g2d.setFont(new Font("Monospaced", Font.BOLD, 18));
        drawText(g2d, "Effect:", x - 20, y + 20, null, ARC_TEXT);

        g2d.setColor(enabled ? ARC_TEXT : ARC_PANEL);
        g2d.fillRect(x, y, 100, 40);
        g2d.setColor(ARC_NEON);
        g2d.drawRect(x, y, 100, 40);
        g2d.setFont(new Font("Monospaced", Font.BOLD, 14));
        drawCenteredText(g2d, "ON", x + 50, y + 20, null);
        g2d.setColor(enabled ? Color.BLACK : ARC_DIM);
        g2d.drawString("ON", x + 50 - g2d.getFontMetrics().stringWidth("ON") / 2, y + 20);

        g2d.setColor(enabled ? ARC_PANEL : ARC_TEXT);
        g2d.fillRect(x + 130, y, 100, 40);
        g2d.setColor(ARC_NEON);
        g2d.drawRect(x + 130, y, 100, 40);
        g2d.setFont(new Font("Monospaced", Font.BOLD, 14));
        drawCenteredText(g2d, "OFF", x + 180, y + 20, null);
        g2d.setColor(enabled ? ARC_DIM : ARC_LIME);
        g2d.drawString("OFF", x + 180 - g2d.getFontMetrics().stringWidth("OFF") / 2, y + 20);

        // Intensity slider
        int barX = W / 2 - 150, barY = 300, barW = 300, barH = 16;
        sliderRect = new int[]{barX, barY, barW, barH};
        float fill = CRTSettings.getIntensity() / 100.0f;

        g2d.setFont(new Font("Monospaced", Font.BOLD, 18));
        drawText(g2d, "Intensity:", barX - 20, barY + 8, null,
                enabled ? ARC_TEXT : ARC_DIM);

        g2d.setColor(ARC_PANEL);
        g2d.fillRect(barX, barY, barW, barH);
        g2d.setColor(enabled ? ARC_TEXT : ARC_PANEL);
        g2d.fillRect(barX, barY, (int) (barW * fill), barH);
        g2d.setColor(enabled ? ARC_NEON : ARC_DIM);
        g2d.drawRect(barX, barY, barW, barH);

        g2d.setFont(new Font("Monospaced", Font.BOLD, 13));
        drawText(g2d, CRTSettings.getIntensity() + "%", barX + barW + 12, barY + 8, null, ARC_NEON);

        // Band legend
        g2d.setFont(new Font("Monospaced", Font.PLAIN, 13));
        g2d.setColor(ARC_DIM);
        drawCenteredText(g2d, "0-33: Scanlines Only   34-66: Plus Vignette   67-100: Plus Flicker",
                W / 2, 360, null);

        // Hints
        drawCenteredText(g2d, "Up/Down to move   Left/Right to adjust   ENTER to confirm   ESC for Options",
                W / 2, H - 80, null);
    }
}
