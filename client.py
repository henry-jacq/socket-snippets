import socket
from time import sleep


class Client:
    data_size = 2048

    commands = ['help', 'exit', 'pwd', 'info', 'shutdown']

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            while True:
                print(f"[+] Trying to connect {self.host}")
                result = self.socket.connect((self.host, self.port))
                if result is None:
                    sleep(1.5)
                    print("[+] Got a Connection!")
                    return True
        except Exception as e:
            sleep(1.5)
            print(f"[-] {e}")
            return False

    def run(self):
        try:
            if self.connect():
                print("[+] Gaining Shell...")
                sleep(.5)
                while True:
                    message = input(">> ")

                    if message.lower() in self.commands:
                        if message.lower() == 'exit':
                            break

                        if message.lower() == 'help':
                            self.print_help()
                            continue

                        if message.lower() == 'info':
                            self.socket.send(message.encode('utf-8'))
                            response = self.socket.recv(self.data_size)
                            print(response.decode('utf-8'))
                            continue

                    elif not message:
                        continue

                    self.socket.send(message.encode('utf-8'))
                    response = self.socket.recv(self.data_size)
                    print(response.decode('utf-8'))

                    if message.lower() == 'shutdown':
                        print("[+] Initiating shutdown process...")
                        self.socket.send(message.encode('utf-8'))
                        break

                print("[-] Connection closed!")
        except:
            self.__close()

    def print_help(self):
        print("Available Commands:")
        print("\tdir - List info about current directory")
        print("\tshutdown - Turn off the remote host")
        print("\tpwd - Print path of current directory")
        print("\tinfo - Print remote host information")
        print("\texit - Exit from the shell")
        print("\thelp - Print this help message")

    def manage_commands(self):
        pass

    def __close(self):
        self.socket.close()
        sleep(0.5)
        print("[-] Pipeline Broken!")


if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    port = 4555

    client = Client(host, port)
    client.run()
