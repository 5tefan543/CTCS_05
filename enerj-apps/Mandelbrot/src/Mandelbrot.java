package src;

import java.awt.image.BufferedImage;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import javax.imageio.ImageIO;

import enerj.lang.*;

public class Mandelbrot {

    private static final String OUTPUT_FOLDER = "output";

    private static final int DEFAULT_SIZE_X = 160;
    private static final int DEFAULT_SIZE_Y = 80;

    private static final int NUM_CHANNELS = 3;
    private static final int MAX_ITER = 7500;

    public static boolean simulate = false;

    public static void main(String[] args) {
        int sizeX = DEFAULT_SIZE_X;
        int sizeY = DEFAULT_SIZE_Y;

        if (args.length >= 2) {
            try {
                sizeX = Integer.parseInt(args[0]);
                sizeY = Integer.parseInt(args[1]);
                if (args.length == 3) {
                    Mandelbrot.simulate = Boolean.parseBoolean(args[2]);
                }
            } catch (NumberFormatException e) {
                System.out.println("Invalid arguments. Using default size and simulate settings.");
            }
        } else {
            System.out.println("No arguments given. Using default size and simulate settings.");
        }

        @Approx byte[] image = new @Approx byte[NUM_CHANNELS * sizeX * sizeY];

        long startTime = System.nanoTime();
        calculateMandelbrot(image, sizeX, sizeY);
        long endTime = System.nanoTime();

        double totalTime = (endTime - startTime) / 1e9;
        if (simulate) {
            printImageToConsole(image, sizeX, sizeY);
        } else {
            saveImage(image, sizeX, sizeY);
            System.out.printf("Mandelbrot set calculation for %dx%d took: %.3f seconds.%n", sizeX, sizeY, totalTime);
        }
    }

    private static void calculateMandelbrot(@Approx byte[] image, int sizeX, int sizeY) {
        @Approx final float left = -2.5f, right = 1.0f;
        @Approx final float bottom = -1.0f, top = 1.0f;

        @Approx RGB rgb = new @Approx RGB();

        for (int pixelY = 0; pixelY < sizeY; pixelY++) {
            // scale y pixel into mandelbrot coordinate system
            @Approx float cy = (pixelY / (float) sizeY) * (top - bottom) + bottom;

            for (int pixelX = 0; pixelX < sizeX; pixelX++) {
                // scale x pixel into mandelbrot coordinate system
                @Approx float cx = (pixelX / (float) sizeX) * (right - left) + left;
                @Approx float x = 0, y = 0;
                int numIterations = 0;

                // Check if the distance from the origin becomes 
			    // greater than 2 within the max number of iterations.
                while ((Endorsements.endorse(x * x + y * y) <= 2*2) && (numIterations < MAX_ITER)) {
                    @Approx float xTmp = x * x - y * y + cx;
                    y = 2 * x * y + cy;
                    x = xTmp;
                    numIterations++;
                }

                double value = Math.abs((numIterations / (double) MAX_ITER)) * 200;
                hsvToRgb(value, 1.0, 1.0, rgb);

                int baseIndex = (pixelY * sizeX + pixelX) * NUM_CHANNELS;
                int channel = 0;
                image[baseIndex + channel++] = (@Approx byte) (rgb.red * 255);
                image[baseIndex + channel++] = (@Approx byte) (rgb.green * 255);
                image[baseIndex + channel++] = (@Approx byte) (rgb.blue * 255);

                // inform about progress
                int currentPixel = pixelY * sizeX + pixelX + 1;
                if (!Mandelbrot.simulate && currentPixel % (sizeX * sizeY / 100) == 0) {
                    System.out.printf("Progress: %.2f%%%n", (currentPixel / (double) (sizeX * sizeY)) * 100);
                }
            }
        }
    }

    private static void hsvToRgb(double h, double s, double v, @Approx RGB rgb) {
        if (h >= 1.0) {
            v = 0.0;
            h = 0.0;
        }

        double step = 1.0 / 6.0;
        double vh = h / step;

        int i = (int) Math.floor(vh);
        double f = vh - i;
        double p = v * (1.0 - s);
        double q = v * (1.0 - (s * f));
        double t = v * (1.0 - (s * (1.0 - f)));

        switch (i) {
            case 0:
                rgb.red = v;
                rgb.green = t;
                rgb.blue = p;
                break;
            case 1:
                rgb.red = q;
                rgb.green = v;
                rgb.blue = p;
                break;
            case 2:
                rgb.red = p;
                rgb.green = v;
                rgb.blue = t;
                break;
            case 3:
                rgb.red = p;
                rgb.green = q;
                rgb.blue = v;
                break;
            case 4:
                rgb.red = t;
                rgb.green = p;
                rgb.blue = v;
                break;
            case 5:
                rgb.red = v;
                rgb.green = p;
                rgb.blue = q;
                break;
        }
    }

    private static void printImageToConsole(@Approx byte[] image, int sizeX, int sizeY) {
        for (int y = 0; y < sizeY; y++) {
            for (int x = 0; x < sizeX; x++) {
                int baseIndex = (y * sizeX + x) * NUM_CHANNELS;
                int r = Endorsements.endorse(image[baseIndex]) & 0xFF;
                int g = Endorsements.endorse(image[baseIndex + 1]) & 0xFF;
                int b = Endorsements.endorse(image[baseIndex + 2]) & 0xFF;

                // Print RGB values
                System.out.printf("(%d, %d, %d) ", r, g, b);
            }
            System.out.println(); // New line for each row
        }
    }

    private static void saveImage(@Approx byte[] image, int sizeX, int sizeY) {
        BufferedImage bufferedImage = new BufferedImage(sizeX, sizeY, BufferedImage.TYPE_INT_RGB);

        for (int y = 0; y < sizeY; y++) {
            for (int x = 0; x < sizeX; x++) {
                int baseIndex = (y * sizeX + x) * NUM_CHANNELS;
                int channel = 0;
                int r = Endorsements.endorse(image[baseIndex + channel++]) & 0xFF;
                int g = Endorsements.endorse(image[baseIndex + channel++]) & 0xFF;
                int b = Endorsements.endorse(image[baseIndex + channel++]) & 0xFF;

                int color = (r << 16) | (g << 8) | b;
                bufferedImage.setRGB(x, y, color);
            }
        }

        try {
            Path outputPath = Paths.get(OUTPUT_FOLDER);
            Files.createDirectories(outputPath); // Creates the directory if it doesn't exist
            String fileName = OUTPUT_FOLDER + "/mandelbrot_" + sizeX + "x" + sizeY + ".png";
            FileOutputStream out = new FileOutputStream(fileName);
            ImageIO.write(bufferedImage, "png", out);
            out.close();
            if(!Mandelbrot.simulate) {
                System.out.println("Image successfully saved to " + fileName);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}