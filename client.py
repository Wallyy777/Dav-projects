import socket
import time
import logging

server_host = '127.0.0.1'
server_port = 55551
REQUEST_CMD = ("DATE", "DATETIME", "TIME")
# Initialize time interval variables
min_interval = 15  # Minimum interval: 15 seconds
max_interval = 3600  # Maximum interval: 1 hour
current_interval = min_interval


# Configure logging
logging.basicConfig(filename='client_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_get_data_message(sock):
    try:
        message = "GET_DATA\n"
        sock.sendall(message.encode("utf-8"))
        return True
    except Exception as e:
        logging.error(f"Error sending GET_DATA message: {str(e)}")
        return False

def handle_post_message(sock):
    response = sock.recv(1024).decode("utf-8")
    print(response)
    transaction_data = ""
    if response.startswith("POST"):
        data = response.split(" ")[1:]
        transaction_data = " ".join(data[1:])
        return transaction_data
    else:
        print("Received an unexpected response from SLD")
        return None
'''  except Exception as e:
        print(f"Error handling POST message: {transaction_data}")
        #logging.error(f"Error handling POST message: {str(e)}")
        return None'''

def adjust_time_interval(response_contains_data):
    global current_interval
    if response_contains_data:
        current_interval = max(min_interval, current_interval // 2)
    else:
        current_interval = min(max_interval, current_interval * 2)

def handle_malformed_message():
    sock.close()
    print(f'Error001: Malformed message recieved from SLD')
    logging.error("Error_001: Malformed message received from SLD.")
    # Implement logic to handle the error and retry or take appropriate action.

def handle_no_response():
    print(f'Failed to contact SLD. Will retry in 15 seconds.')
    logging.warning("Failed to contact SLD. Will retry in 15 seconds.")
    # Implement logic to handle the error and retry or take appropriate action.

if __name__ == "__main__":
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_host, server_port))
        
        if send_get_data_message(sock):
            transaction_data = handle_post_message(sock)
            
            if transaction_data != "" and len(transaction_data) > 4:
                print(f"Received response: {transaction_data}")
                logging.info(f"Received transaction data: {transaction_data}")
                message2 = "CLEAR_DATA\n"
                sock.sendall(message2.encode("utf-8"))
                
            else:
                
                handle_malformed_message()
                adjust_time_interval(bool(transaction_data))
                logging.info(f"Next attempt in {current_interval} seconds")
                time.sleep(current_interval)
                sock.close()
        else:
            handle_no_response()
            sock.close()

        adjust_time_interval(bool(transaction_data))
        logging.info(f"Next attempt in {current_interval} seconds")
        time.sleep(current_interval)