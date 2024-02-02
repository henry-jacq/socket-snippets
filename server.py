import socket

class Backdoor:
    data_size = 2048

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = None
        self.client = None
        self.socket.bind((host, port))

    def listen(self):
        self.socket.listen()
        print(f"Backdoor listening on {host}:{port}")

    def start(self):
        while True:
            if self.addr is None and self.client is None:
                client_socket, addr = self.socket.accept()
                self.addr = addr[0]
                self.client = client_socket
                print(f"Got a connection from {self.addr}")
                print("Waiting to receive data from client..")

            data = self.client.recv(self.data_size)
            if not data:
                print("Breaking!")
                print(data)
                self.__stop()
                break

            # Print the received data
            print("[*] DATA:", data.decode('utf-8'))

            # Send a response back to the client
            response = "Message received successfully"
            client_socket.send(response.encode('utf-8'))

    def __stop(self):
        # Close the connection
        self.socket.close()
        print("Closing connection...")



if __name__ == "__main__":
    host = socket.gethostname()
    port = 12345

    b = Backdoor(host, port)
    b.listen()
    b.start()
