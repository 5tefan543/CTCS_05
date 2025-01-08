package src;

import enerj.lang.*;

public class HeatStencil2D {

    static final int RESOLUTION_x = 50;
    static final int RESOLUTION_y = 50;

    public static void main(String[] args) {
        int N_x = 768;
        int N_y = 768;

        if (args.length < 2) {
            System.out.println("ERROR: Not enough arguments");
            return;
        }
        if (args.length >= 2) {
            N_x = Integer.parseInt(args[0]);
            N_y = Integer.parseInt(args[1]);
        }

        int T = N_x * 100;
        System.out.printf("Computing heat-distribution for room size N = %d x %d for T=%d timesteps\n", N_x, N_y, T);

        @Approx double[][] A = new @Approx double[N_y][N_x];

        for (int i = 0; i < N_y; i++) {
            for (int j = 0; j < N_x; j++) { 
                A[i][j] = 273; // temperature is 0 C everywhere (273 K) 
            }
        }

        int source_x = N_x / 4;
        int source_y = N_y / 4;
        A[source_y][source_x] = 273 + 60;

        System.out.println("Initial:");
        printTemperature(A, N_x, N_y);
        System.out.println();

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

            if(t % 100 == 0){
                if (t % 1000 == 0) {
                    System.out.printf("Step t=%d:\n", t);
                    printTemperature(A, N_x, N_y);
                    System.out.println();
                } else {
                    System.out.printf("Timestep %d complete. \n", t);
                }
            }
            
        }

        System.out.println("Final:");
        printTemperature(A, N_x, N_y);
        System.out.println();

        boolean success = true;
        for (int i = 0; i < N_y; i++) {
            for (int j = 0; j < N_x; j++) {
                double temp = Endorsements.endorse(A[i][j]);
                if (273 <= temp && temp <= 273 + 60) continue;
                success = false;
                break;
            }
        }

        System.out.println("Verification: " + (success ? "OK" : "FAILED"));
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
