import java.io.*;
import enerj.lang.*;

public class HelloWorld {
        static @Approx int a = 878;
        static @Approx int b = 55;
        static @Approx int sum = 0;
        static @Precise int N = 10;
        public static void main(String[] argv) {
                for(int i = 0; i < N; i++) {
                        sum += a+b; 
                }
                System.out.printf("(%d+%d)*%d=%d\n", Endorsements.endorse(a), Endorsements.endorse(b), N, Endorsements.endorse(sum));
        }
}