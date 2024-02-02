import socket

class Backdoor:
    data_size = 2048

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = None
        self.addr = None
        self.socket.bind((host, port))

    def listen(self):
        self.socket.listen(1)
        print(f"==> Backdoor listening on {host}:{port}")

    def run(self):
        if self.listen() is not None:
            self.__stop()
            return
        while True:
            if self.addr is None and self.client is None:
                client_socket, addr = self.socket.accept()
                self.addr = addr
                self.client = client_socket
                print(f"[+] Got a connection from {addr[0]}")
                print("[!] Waiting to receive data from client..")

            data = self.client.recv(self.data_size)

            if not data:
                self.__stop()
                break

            # Print the received data
            print("[*] DATA:", data.decode('utf-8'))
            print(f"Received {len(data)} bytes")

            self.client.send(data)

    def __stop(self):
        # Close the connection
        self.socket.close()
        print(f"[-] Closing connection {self.addr[0]}")



if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    port = 12345

    b = Backdoor(host, port)
    b.run()
