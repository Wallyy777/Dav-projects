import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Scanner;

public class Server {

    // constants
    private static final int ARGS_LENGTH = 3;
    private static final String ending = "\n";
    private static final String errorMessage = "ERROR_001\n";
    private static final String clearMessage = "CLEAR_DATA\n";
    private static final String getDataMessage = "GET_DATA\n";

    private static final String emptyPost = "POST\n";

    private static final int ERROR = -1, GET = 1, CLEAR = 2, NOTICE = 3, EMPTY = 4;

    // static fields.
    private static int portNumber = 23457;
    private static int cacheCounter = 0;
    private static double errorProbability = 0.5;
    private static String[] cachedTransactions = new String[] {
            "POST 1234123412341234 01/79 07/07/2077 025.32 08:31:25 01:12:05\n",
            "Post: this is a badly formatted post message.\n",
            "POST 2345234523452345 02/83 07/07/2077 018.87 10:25:01 00:45:58\n",
            "POST 3456345634563456 03/78 07/07/2077 031.20 11:45:19 02:00:00\n",
            "POST 4567456745674567 04/81 07/07/2077 019.90 13:53:33 01:00:00\n",
            "POST 5678567856785678 10/77 07/07/2077 019.88 15:07:59 00:29:59\n",
            emptyPost, // indicates there is no transaction information.
            "POST 7890789078907890 12/77 07/07/2077 025.25 16:03:33 01:00:00\n",
            "POST 6789678967896789 08/77 07/07/2077 003.16 17:21:41 00:45:00\n",
            emptyPost // indicates there is no transaction information.
    };

    public static void main(String[] args) {
        setUp(args);
        try (ServerSocket serverSocket = new ServerSocket(portNumber)) {
            while (true) {
                try (Socket clientSocket = serverSocket.accept();
                        PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
                        BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()))) {
                    handleProtocol(in, out);
                } catch (Exception e) {
                    throw new RuntimeException(e);
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static void handleProtocol(BufferedReader in, PrintWriter out) throws IOException {
        int initialRequest = readMessage(in);
        if (initialRequest == NOTICE)
            return; // error message
        if (initialRequest != GET) {
            System.out.println("Bad Protocol.");
            // return;
        }
        boolean sentData = sendData(out);
        int secondRequest = readMessage(in);
        if (secondRequest == NOTICE) {
            clearCache();
        } else if (secondRequest == CLEAR && !cachedTransactions[cacheCounter].equals(emptyPost)) {
            clearCache();
        } else if (secondRequest == EMPTY && cachedTransactions[cacheCounter].equals(emptyPost)) {
            clearCache();
        } else if (secondRequest == EMPTY && !sentData) {
            // do nothing.
        } else {
            System.out.println("Bad Protocol.");
        }
    }

    private static void clearCache() {
        cacheCounter = Math.min(cacheCounter + 1, cachedTransactions.length - 1);
        System.out.println("Cleared one transaction/moving SLD simulation forward one transaction");
    }

    // return 1 for get data
    // return 2 for clear
    // return 3 for error 001
    // return 0 for no message.
    // return -1 for bad message
    private static int readMessage(BufferedReader in) throws IOException {
        char[] buffer = new char[64]; // client message will always be less than 64 chars long.
        int length = in.read(buffer);
        if (length < 0) {
            System.out.println("Server received no message.");
            return EMPTY;
        }
        String message = new String(buffer, 0, length);
        System.out.println("Server Received: \"" + message + "\"...");
        if (message.equals(getDataMessage)) {
            System.out.println("\t...that is a data request.");
            return GET;
        }
        if (message.equals(clearMessage)) {
            System.out.println("\t... that is a clear request.");
            return CLEAR;
        }
        if (message.equals(errorMessage)) {
            System.out.println("\t... that is an error notification.");
            return NOTICE;
        }
        System.out.println("\t... that is a badly formatted message.");
        return ERROR;
    }

    private static boolean sendData(PrintWriter out) {
        int delay = (int) (Math.random() * 10000);
        boolean willSend = Math.random() > errorProbability;
        if (!willSend) {
            System.out.println("Server failed to send data.");
            return false;
        }
        try {
            Thread.sleep(delay);
        } catch (InterruptedException ie) {
            System.out.println("If you are seeing this message, let Prof. Olsen know immediately.");
        }
        out.print(cachedTransactions[cacheCounter]);
        out.flush();
        System.out.println("Server sent " + cachedTransactions[cacheCounter]);
        return true;
    }

    private static void setUp(String[] args) {
        if (args.length != ARGS_LENGTH) {
            printHelp();
            System.exit(0);
        }
        System.out.println("Setting up server...");
        portNumber = 23457;// Integer.parseInt(args[0]);
        System.out.println("Port number: " + portNumber);
        errorProbability = 0.5;// Double.parseDouble(args[1]);
        System.out.println("Probability of lost GET_DATA message: " + errorProbability);
        try {
            Scanner transactionsIn = new Scanner(new File(args[2]));
            ArrayList<String> transactions = new ArrayList<String>();
            while (transactionsIn.hasNextLine()) {
                transactions.add(transactionsIn.nextLine() + "\n");
            }
            cachedTransactions = transactions.toArray(cachedTransactions);
        } catch (FileNotFoundException e) {
            System.out.println("Could not open file.  Using default transactions.");
        }
        System.out.println("Cached Transactions: ");
        for (String s : cachedTransactions) {
            System.out.print(s);
        }
    }

    private static void printHelp() {
        System.out.println("Usage: <name of executable> <port number> <lost GET_DATA probability> <transactions file>");
    }
}