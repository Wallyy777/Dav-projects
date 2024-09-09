import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.atomic.AtomicInteger;

//Davonta Wallace Assignment 5 CSC 445
public class LaundryServer {

    public static void main(String[] args) {
        int port = 23456; // Choose a port of your preference
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(1);
        List<String> responses = new ArrayList<String>();
        responses.add("POST 1234123412341234 01/29 07/07/2077 25.32 08:31:25 01:12:05");
        responses.add("POST 4229222781862224 01/9 17/57/2077 25.32 08:31:25 01:12:05");
        responses.add("POST 7234123412341234 11/30 05/22/2047 25.32 08:31:25 01:12:05");
        responses.add("POST 377612341234779h 01/27 07/07/2021 25.32 08:31:25 01:12:05");
        responses.add("POST 8776123412347795 08/25 07/77/2021 25.32 08:31:25 01:12:05");
        responses.add("POST 1234432112341234 11/30 05/25/2047 25.8 08:31:25 01:12:05");
        responses.add("POST 9876123412341234 11/30 05/22/2047 25.32 08:3:25 01:12:05");
        responses.add("POST 8743532573537890 11/30 05/22/2047 25.32 08:31:25 01:1:05");
        responses.add("POST 7234123412341234 11/30 05/22/2047 25.32 08:31:25 01:12:05");

        try (ServerSocket serverSocket = new ServerSocket(port)) {
            System.out.println("Laundry Server is running on port " + port);
            AtomicInteger responseIndex = new AtomicInteger(0);
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Client connected: " + clientSocket.getInetAddress());

                // Create a new thread to handle the client
                Runnable clientHandler = () -> {
                    try {
                        BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                        PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

                        String request = in.readLine();

                        if (request != null && request.equals("GET_DATA")) {
                            // Send the next response from the list
                            String response = responses.get(responseIndex.get());
                            responseIndex.set((responseIndex.get() + 1) % responses.size()); // Cycle through responses
                            System.out.println("Server ACKNOWLEDGED message: 'GET_DATA'\n");
                            out.println(response);
                            System.out.println("Responded to GET_DATA request.\n");
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    } finally {
                        try {
                            clientSocket.close();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                };

                // Create a new thread to handle the client
                Thread clientThread = new Thread(clientHandler);
                clientThread.start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}