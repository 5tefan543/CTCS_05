package src;

import enerj.lang.*;
import java.io.FileWriter;
import java.io.IOException;

public class HeatStencil2D {

    static final int RESOLUTION_x = 25;
    static final int RESOLUTION_y = 25;

    public static void main(String[] args) {
        int N_x = 768;
        int N_y = 768;
        int outputMode = 0;

        if (args.length < 2) {
            System.out.println("ERROR: Not enough arguments");
            System.out.println("Usage: java HeatStencil2D <N_x> <N_y> [outputMode]");
            System.out.println("outputMode: 0 for printing (default), 1 for writing to CSV, 2 for benchmarking print");
            return;
        }

        N_x = Integer.parseInt(args[0]);
        N_y = Integer.parseInt(args[1]);
        
        if (args.length >= 3) {
            outputMode = Integer.parseInt(args[2]);
            if(0 > outputMode || outputMode > 3){
                outputMode = 0;
            }
        }

        int T = N_x * 100;
        if(outputMode != 2){
            System.out.printf("Computing heat-distribution for room size N = %d x %d for T=%d timesteps\n", N_x, N_y, T);
        }
        if(outputMode == 1){
            System.out.println("Writing results to temperatures.csv");
        } else if(outputMode == 0) {
            System.out.println("Printing output to Terminal");
        }

        @Approx double[][] A = new @Approx double[N_y][N_x];

        for (int i = 0; i < N_y; i++) {
            for (int j = 0; j < N_x; j++) { 
                A[i][j] = 273; // temperature is 0 C everywhere (273 K) 
            }
        }

        int source_x = N_x / 4;
        int source_y = N_y / 4;
        A[source_y][source_x] = 273 + 60;

        FileWriter writer = null;

        try{
            if (outputMode== 1) {
                writer = new FileWriter("temperatures.csv");
            }

            if(outputMode == 0){
                System.out.println("Initial:");
                printTemperature(A, N_x, N_y);
                System.out.println();
            } else if(outputMode == 1){
                writeArrayToFile(writer, A, N_x, N_y, 0);
                writer.flush();
            }

            @Approx double[][] B = new @Approx double[N_y][N_x];

            for (int t = 1; t < T; t++) {
                for (int i = 0; i < N_y; i++) {
                    for (int j = 0; j < N_x; j++) {
                        if (i == source_y && j == source_x) {
                            B[i][j] = A[i][j];
                            continue;
                        }

                        @Approx double tc = A[i][j];
                        @Approx double tu = (i != 0) ? A[i - 1][j] : tc;
                        @Approx double td = (i != N_y - 1) ? A[i + 1][j] : tc;
                        @Approx double tl = (j != 0) ? A[i][j - 1] : tc;
                        @Approx double tr = (j != N_x - 1) ? A[i][j + 1] : tc;

                        B[i][j] = tc + 0.167 * (tl + tr + tu + td + (-4 * tc));
                    }
                }

                @Approx double[][] H = A;
                A = B;
                B = H;

                if(outputMode == 1 && t <= 10){
                    writeArrayToFile(writer, A, N_x, N_y, t);
                    writer.flush();
                }
                if(t % 100 == 0){
                    if (t % 1000 == 0) {
                        if(outputMode == 1){
                            writeArrayToFile(writer, A, N_x, N_y, t);
                            writer.flush();
                        } else if (outputMode == 0){
                            System.out.printf("Step t=%d:\n", t);
                            printTemperature(A, N_x, N_y);
                            System.out.println();
                        }
                    } else if (outputMode == 0) {
                        System.out.printf("Timestep %d complete. \n", t);
                    }
                }
                
            }

           if(outputMode == 1) {
                writeArrayToFile(writer, A, N_x, N_y, T);
                writer.flush();
            } else if(outputMode == 2){
                for (int i = 0; i < N_y; i++) {
                    for (int j = 0; j < N_x; j++) {
                        System.out.printf(String.format("%.2f", Endorsements.endorse(A[i][j])));
                        if (j < N_x - 1) {
                            System.out.print(" ");
                        }
                    }
                    System.out.printf("\n");
                }
                System.out.printf("\n");
            } else{
                System.out.println("Final:");
                printTemperature(A, N_x, N_y);
                System.out.println();
            }
        } catch (IOException e){
            System.out.println("ERROR: Could not write to file.");
            e.printStackTrace();
        }

        boolean success = true;
        for (int i = 0; i < N_y; i++) {
            for (int j = 0; j < N_x; j++) {
                double temp = Endorsements.endorse(A[i][j]);
                if (273 <= temp && temp <= 273 + 60) continue;
                success = false;
                break;
            }
        }

        if(outputMode == 0 || outputMode == 1){
            System.out.println("Verification: " + (success ? "OK" : "FAILED"));
        }
    }

    static void writeArrayToFile(FileWriter writer, @Approx double[][] matrix, int N_x, int N_y, int timestep) throws IOException {
        writer.write("Timestep " + timestep + "\n");
        for (int i = 0; i < N_y; i++) {
            for (int j = 0; j < N_x; j++) {
                writer.write(String.format("%.2f", Endorsements.endorse(matrix[i][j])));
                if (j < N_x - 1) {
                    writer.write(",");
                }
            }
            writer.write("\n");
        }
        writer.write("\n");
    }

    static void printTemperature(@Approx double[][] m, int N_x, int N_y) {
        final String colors = " .-:=+*^X#%@";
        final int numColors = 12;

        final double max = 273 + 30;
        final double min = 273 + 0;

        int W_x = RESOLUTION_x;
        int W_y = RESOLUTION_y;

        int sW_x = N_x / W_x;
        int sW_y = N_y / W_y;

        for (int i = 0; i < W_y; i++) {
            System.out.print("X");
            for (int j = 0; j < W_x; j++) {
                double max_t = 0;
                for (int y = sW_y * i; y < sW_y * (i + 1); y++) {
                    for (int x = sW_x * j; x < sW_x * (j + 1); x++) {
                        max_t = Math.max(max_t, Endorsements.endorse(m[y][x]));
                    }
                }

                double temp = max_t;
                int c = (int) ((temp - min) / (max - min) * numColors);
                c = Math.min(Math.max(c, 0), numColors - 1);

                System.out.print(colors.charAt(c));
            }
            System.out.println("X");
        }
    }
}
