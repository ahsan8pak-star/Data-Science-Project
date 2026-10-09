// Global CRT Visual Effect Settings and Drawing Utility
// Inspired by retro arcade monitor aesthetics, referenced from: https://perchance.org/text-adventure-template

// The CRT effect draws horizontal scanlines and a corner vignette
// Over the game content to simulate the look of an old arcade CRT monitor.
// It is applied as the final draw call in minigame paintComponent methods.

// Intensity 0 = No Effect (completely off)
// Intensity 1-33 = Light Scanlines Only
// Intensity 34-66 = Scanlines + Vignette
// Intensity 67-100 = Scanlines + Vignette + Subtle Flicker Overlay

import java.awt.Color;
import java.awt.GradientPaint;
import java.awt.Graphics2D;
import java.awt.RadialGradientPaint;
import java.awt.RenderingHints;
import java.awt.geom.Point2D;

public class CRTSettings {

    // Whether the CRT Effect is Enabled at All
    private static boolean enabled = false;

    // Intensity 0-100 (0 = None, 100 = Maximum)
    private static int intensity = 40;

    // Internal Flicker Counter (Incremented Each drawCRT Call)
    private static int flickTick = 0;

    // Getters / Setters
    public static boolean isEnabled() {
        return enabled;
    }

    public static void setEnabled(boolean b) {
        enabled = b;
    }

    public static int getIntensity() {
        return intensity;
    }

    public static void setIntensity(int v) {
        intensity = Math.max(0, Math.min(100, v));
    }

    public static void toggle() {
        enabled = !enabled;
    }

    // Draw the CRT overlay on top of all game content.
    // Call this as the LAST operation in paintComponent.
    // Does nothing if CRT is disabled or intensity is 0.

    // @param g2d Graphics2D context of the panel
    // @param w Panel pixel width
    // @param h Panel pixel height

    public static void drawCRT(Graphics2D g2d, int w, int h) {
        if (!enabled || intensity <= 0)
            return;

        try {
            g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                    RenderingHints.VALUE_ANTIALIAS_OFF);

            float alpha = intensity / 100.0f;

            // Layer 1: Horizontal Scanlines
            // Dark bands every 2 pixels simulate CRT phosphor row gaps
            // Opacity scales with intensity (min 0.08, max 0.45)
            float scanAlpha = 0.08f + alpha * 0.37f;
            Color scanColor = new Color(0f, 0f, 0f, Math.min(1.0f, scanAlpha));
            g2d.setColor(scanColor);
            for (int y = 0; y < h; y += 2) {
                g2d.drawLine(0, y, w, y);
            }

            // Layer 2: Vignette (Darkened Corners)
            // Only applied when intensity >= 34
            if (intensity >= 34) {
                float vigAlpha = Math.min(0.70f, alpha * 0.75f);
                float[] fractions = { 0.0f, 0.55f, 1.0f };
                Color[] colors = {
                        new Color(0f, 0f, 0f, 0.0f),
                        new Color(0f, 0f, 0f, 0.0f),
                        new Color(0f, 0f, 0f, vigAlpha)
                };
                float cx = w / 2.0f, cy = h / 2.0f;
                float radius = (float) Math.sqrt(cx * cx + cy * cy);
                try {
                    RadialGradientPaint vignette = new RadialGradientPaint(
                            new Point2D.Float(cx, cy),
                            radius,
                            fractions,
                            colors);
                    g2d.setPaint(vignette);
                    g2d.fillRect(0, 0, w, h);
                } catch (Exception ignored) {
                    // RadialGradientPaint can fail with tiny panels - skip vignette
                }
            }

            // Layer 3: Flicker Overlay
            // Only applied when intensity >= 67
            // Adds a very subtle periodic brightness variation
            if (intensity >= 67) {
                flickTick++;
                // Flicker cycles every ~20 frames; most frames transparent
                if (flickTick % 20 == 0) {
                    float flickAlpha = 0.03f + (float) (Math.random() * 0.04f);
                    g2d.setColor(new Color(0f, 0.8f, 0f, flickAlpha)); // Green tint flicker
                    g2d.fillRect(0, 0, w, h);
                }
            }

            // Layer 4: Subtle Green Phosphor Tint
            // Applied at all intensity levels to give a slight green-screen glow
            float tintAlpha = alpha * 0.04f;
            g2d.setColor(new Color(0f, 1.0f, 0f, Math.min(0.08f, tintAlpha)));
            g2d.fillRect(0, 0, w, h);

        } catch (Exception e) {
            // Silently Ignore Any Rendering Errors - Game Is Unaffected
        } finally {
            g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                    RenderingHints.VALUE_ANTIALIAS_ON);
        }
    }
}
