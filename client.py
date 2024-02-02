import socket

class Client:
    data_size = 1024

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def ask_input(self):
        while True:
            message = input("Enter your message: ")
            self.socket.send(message.encode('utf-8'))
            response = self.socket.recv(self.data_size)
            print("Response from server:", response.decode('utf-8'))

    def __close(self):
        self.socket.close()
        print("Pipeline Broken!")

if __name__ == "__main__":
    host = socket.gethostname()
    port = 12345

    client = Client(host, port)

    client.ask_input()
