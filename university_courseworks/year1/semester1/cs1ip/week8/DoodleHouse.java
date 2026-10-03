import javax.swing.*;        
import java.awt.*;

// Greetings card with a drawing of a house.

class DoodlePanel extends JPanel {

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Draw the sky.
        g.setColor(Color.CYAN);
        g.fillRect(0,0,640,480);

        // Draw the grass.
        g.setColor(Color.GREEN);
        g.fillRect(0,400,640,80);

        // Draw outline of the house.
        g.setColor(Color.WHITE);
        g.fillRect(170,280,300,200);

        // Draw the door.
        g.setColor(Color.RED);
        g.fillRect(300,380,40,100);

        // Draw two windows.
        drawWindow(g, 220,380);
        drawWindow(g, 370,380);

        // Draw the roof.
        g.setColor(Color.DARK_GRAY);
        g.fillPolygon(new int[] {170, 470, 420, 220}, new int[] {280, 280, 230, 230}, 4);

        // Draw the sun.
        drawSun(g, 530, 140, 10);

        // Draw a greeting.
        g.setColor(Color.MAGENTA);
        g.setFont(g.getFont().deriveFont(40.0f));
        g.drawString("Happy Housewarming", 50, 100);

    }

    // Use separate functions for the more complicated parts of the drawing:

    // Draw a window at (x,y).
    protected void drawWindow(Graphics g, int x, int y) {
        // Move to the corner of the window.
        g.translate(x, y);
        // Draw the window outline.
        g.setColor(Color.BLUE);
        g.fillRect(0,0,50,50);
        // Draw lines to separate the window into panes.
        g.setColor(Color.BLACK);
        g.drawLine(25,0,25,50);
        g.drawLine(0,25,50,25);
        // Move back to the origin.
        g.translate(-x, -y);
    }

    // Draw the sun at (x,y) with the specified number of rays.
    protected void drawSun(Graphics g, int x, int y, int rays) {
        // Move to the centre of the sun.
        g.translate(x, y);
        // Draw the centre of the sun.
        g.setColor(Color.YELLOW);
        g.fillOval(-50, -50, 100, 100);
        // Draw individual rays.
        for (int n = 0; n < rays; n++) {
            // Calculate the angle of the ray.
            double angle = (360.0 / rays) * n;
            double rads_per_degree = Math.PI * 2.0 / 360.0;
            double length = 100.0;
            // Draw the ray.
            g.drawLine(0,0, (int) (length * Math.cos(angle * rads_per_degree)), (int) (length * Math.sin(angle * rads_per_degree)));
        }
        // Move back to the origin.
        g.translate(-x, -y);
    }


}

///////////////////////////////////////////////////////////////////////////////
// You can ignore everything below here.
// It just sets up a window pained using the code above.
///////////////////////////////////////////////////////////////////////////////

// Adapted from:
// https://docs.oracle.com/javase/tutorial/uiswing/examples/start/HelloWorldSwingProject/src/start/HelloWorldSwing.java

public class DoodleHouse {

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
