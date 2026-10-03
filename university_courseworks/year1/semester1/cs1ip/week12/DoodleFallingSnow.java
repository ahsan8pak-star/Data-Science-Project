import javax.swing.*;        
import java.awt.*;
import java.awt.geom.AffineTransform;
import java.util.Random;
import java.util.ArrayList;

class DoodlePanel extends JPanel {

    int frame;
    Random r = new Random();

    ArrayList<Integer> snow_y = new ArrayList<Integer>();
    ArrayList<Integer> snow_x = new ArrayList<Integer>();
    ArrayList<Integer> snow_vel = new ArrayList<Integer>();
    ArrayList<Integer> snow_size = new ArrayList<Integer>();
    ArrayList<Integer> snow_spin = new ArrayList<Integer>();
    ArrayList<Integer> snow_col = new ArrayList<Integer>();


    public DoodlePanel() {
        int fps = 25;
        frame = 100;
        Timer t = new Timer(1000/fps, e -> {
            repaint();
        });
        t.start();

    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        frame++;

        // Set up the colours for snowflakes.
        Color col[] = {Color.WHITE, Color.LIGHT_GRAY, Color.DARK_GRAY, Color.CYAN, Color.BLUE};

        if (r.nextInt(30) == 0) {
            snow_x.add(r.nextInt(540) + 50);
            snow_y.add(-150);
            snow_size.add(r.nextInt(100) + 50);
            snow_spin.add(r.nextInt(360));
            snow_vel.add(r.nextInt(4) + 1);
            snow_col.add(r.nextInt(col.length));
        }


        // Draw the night sky.
        g.setColor(Color.BLACK);
        g.fillRect(0,0,640,480);

        // Draw some snowflakes.
        //drawSimpleSnowflake(g, Color.WHITE, 100, 100, 50, 0);
        //drawSimpleSnowflake(g, Color.DARK_GRAY, 175, 200, 75, 10);

        // Draw some snowflakes:
        for (int n = 0; n < snow_x.size(); n++) {
            // Pick a random colour.
            // Position should not be too close to the edge of the screen.
            // Size can be between 50 and 149.
            //int size = r.nextInt(100) + 50;
            //int spin = r.nextInt(360);
            // Actually draw the snowflake.
            drawComplexSnowflake(g, col[snow_col.get(n)], snow_x.get(n), snow_y.get(n), snow_size.get(n), snow_spin.get(n));
            snow_y.set(n, snow_y.get(n) + snow_vel.get(n));
            if (snow_y.get(n) > 600) {
                snow_x.remove(n);
                snow_y.remove(n);
                snow_col.remove(n);
                snow_size.remove(n);
                snow_spin.remove(n);
                snow_vel.remove(n);
                n--;
            }
        }

        // Draw a greeting.
        g.setColor(Color.RED);
        Font originalFont = g.getFont();
        g.setFont(originalFont.deriveFont(40.0f));
        g.drawString("Merry Christmas", 200, 50);
        g.setFont(originalFont);

        g.setColor(Color.GREEN);
        g.drawString("Frame " + frame, 0, 450);
        g.drawString("Snowflakes " + snow_x.size(), 0, 470);

    }

    protected void drawSimpleSnowflake(Graphics g, Color c, int x, int y, int size, int spin) {
        // Set the colour and move the origin to the centre of the snowflake.
        g.setColor(c);
        g.translate(x, y);
        // Draw 6 rays.
        for (int n = 0; n < 6; n++) {
            // Calculate the angle and length of each ray.
            double angle = spin + ((360.0 / 6) * n);
            double rads_per_degree = Math.PI * 2.0 / 360.0;
            double length = size;
            // Draw the ray.
            g.drawLine(0,0, (int) (length * Math.cos(angle * rads_per_degree)), (int) (length * Math.sin(angle * rads_per_degree)));
        }
        // Restore the origin.
        g.translate(-x, -y);

    }

    protected void drawComplexSnowflake(Graphics g0, Color c, int x, int y, int size, int spin) {
        // Set the colour and move the origin to the centre of the snowflake.
        Graphics2D g = (Graphics2D) g0;
        g.setColor(c);
        g.setStroke(new BasicStroke(4.0f));

        AffineTransform original = g.getTransform();
        g.translate(x, y);
        g.rotate(Math.PI * 2.0 * spin / 360.0);
        // Draw 6 rays.
        for (int n = 0; n < 6; n++) {
            // Draw the ray.
            drawComplexFrond(g, size, 3);
            // Rotate to next ray.
            g.rotate(Math.PI * 2.0 / 6.0);
        }
        // Restore the origin.
        g.setTransform(original);

    }

    protected void drawComplexFrond(Graphics2D g, int size, int complexity) {
        if (complexity == 0) {
            return;
        }

        AffineTransform original = g.getTransform();

        g.drawLine(0,0,0,size);

        g.translate(0, size*2/3);
        g.rotate(Math.PI * 2.0 / 6.0);
        drawComplexFrond(g, size/3, complexity-1);
        g.setTransform(original);

        g.translate(0, size*2/3);
        g.rotate(-Math.PI * 2.0 / 6.0);
        drawComplexFrond(g, size/3, complexity-1);
        g.setTransform(original);

        g.translate(0, size*1/3);
        g.rotate(Math.PI * 2.0 / 6.0);
        drawComplexFrond(g, size/4, complexity-1);
        g.setTransform(original);

        g.translate(0, size*1/3);
        g.rotate(-Math.PI * 2.0 / 6.0);
        drawComplexFrond(g, size/4, complexity-1);
        g.setTransform(original);

    }


}

///////////////////////////////////////////////////////////////////////////////
// You can ignore everything below here.
// It just sets up a window pained using the code above.
///////////////////////////////////////////////////////////////////////////////

// Adapted from:
// https://docs.oracle.com/javase/tutorial/uiswing/examples/start/HelloWorldSwingProject/src/start/HelloWorldSwing.java

public class DoodleFallingSnow {

    // Create the GUI and show it.
    // For thread safety, this method should be invoked from the event-dispatching thread.
    private static void createAndShowGUI() {
        // Create and set up the window.
        JFrame frame = new JFrame("HelloWorldSwing");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Add the drawing panel.
        JPanel panel = new DoodlePanel();
        frame.getContentPane().add(panel);
        // Set the size of the drawing panel.
        panel.setPreferredSize(new Dimension(640, 480));

        //Display the window.
        frame.pack();
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        // Schedule a job for the event-dispatching thread:
        // creating and showing this application's GUI.
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                createAndShowGUI();
            }
        });
    }

}
