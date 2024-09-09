
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class Client {
    public static void main(String[] args) {
        final String serverAddress = "127.0.0.1";
        final int goodFullPostLength = "POST 1234123412341234 01/79 07/07/2077 25.32 08:31:25 01:12:05".length();
        final int goodEmptyPostLength = "WORD".length();
        final int serverPort = 23456;
        long interval = 1000; // 0.5 seconds //60000; // 60 seconds
        final long responseTimeout = 15; // 15 seconds
        while (true) {
            try {
                final Socket socket = new Socket();
                socket.connect(new InetSocketAddress(serverAddress, serverPort),
                        (int) TimeUnit.SECONDS.toMillis(responseTimeout));

                final PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                final BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                // Send "GET_DATA" message to the server
                out.println("GET_DATA");

                // Wait for the server's response
                String response = in.readLine();
                boolean skipClear = false;
                String prevresponse;
                List responses = new ArrayList<String>();
                if (response != null) {
                    prevresponse = response;
                    responses.add(prevresponse);
                    String[] tempresponse = response.split(" ");

                    System.out.println("\n" + "Server response: " + response);
                    System.out.println("\"" + response + "\"" + response.length());
                    System.out.println("vs" + goodFullPostLength);
                    if (response.length() != goodEmptyPostLength && response.length() != goodFullPostLength) {
                        System.out.println("got an evil post." + "\n");
                        skipClear = true;
                        out.println("ERROR_001");
                    }
                    if (response.equals("POST") && interval < 30 * 60 * 1000) {
                        skipClear = true;
                        interval *= 2;
                    } else if (interval > 5000) {
                        interval /= 2;
                    }
                    // Check tempresponse[0] equals POST
                    if (!tempresponse[0].equals("POST")) {
                        System.out.println("Invalid POST type");
                        continue;
                    }

                    // Check tempresponse[1] is a 16-digit integer
                    if (!tempresponse[1].matches("\\d{16}")) {
                        System.out.println("Invalid 16-digit integer" + "\n");
                        System.out.println(tempresponse[1]);
                        continue;
                    }

                    // Check tempresponse[2] format (MM/DD)
                    if (!tempresponse[2].matches("(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])")) {
                        System.out.println("Invalid date format" + "\n");
                        System.out.println(tempresponse[2]);
                        continue;
                    }

                    // Check tempresponse[3] format (MM/DD/YYYY)
                    if (!tempresponse[3].matches("(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\\d{4}")) {
                        System.out.println("Invalid date format" + "\n");
                        System.out.println(tempresponse[3]);
                        continue;
                    }
                    // Check tempresponse[4] is a four-digit float
                    if (!tempresponse[4].matches("\\d{2}\\.\\d{2}")) {
                        System.out.println("Invalid float format" + "\n");
                        System.out.println(tempresponse[4]);
                        continue;
                    }

                    // Check tempresponse[5] format (HH:mm:ss)
                    if (!tempresponse[5].matches("([01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d")) {
                        System.out.println("Invalid time format" + "\n");
                        System.out.println(tempresponse[5]);
                        continue;
                    }

                    System.out.println("All validations passed!");

                    if (responses.indexOf(prevresponse) != responses.lastIndexOf(prevresponse)) {
                        System.out.println("Client received duplicate message:\n" + prevresponse + "\n");
                        skipClear = false;
                    }
                } else {
                    System.out.println("Server did not respond.");
                }

                // Send "CLEAR_DATA" message to the server
                if (skipClear == false) {
                    out.println("CLEAR_DATA");
                    out.close();
                }
            } catch (IOException e) {
                System.err.println("Error connecting to the server: " + e.getMessage());
            }
            try {
                Thread.sleep(interval);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }
}