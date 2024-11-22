import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

class SecureClient:
    def __init__(self, server_ip, server_port, agent_token):
        self.server_ip = server_ip
        self.server_port = server_port
        self.agent_token = agent_token
        self.session_key = os.urandom(32)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.server_ip, self.server_port))
            print(f"Connected to server {self.server_ip}:{self.server_port}")

            # Step 1: Receive server's public key
            public_key_bytes = client_socket.recv(1024)
            server_public_key = serialization.load_pem_public_key(public_key_bytes)

            # Step 2: Send agent token
            client_socket.sendall(self.agent_token.encode())

            # Step 3: Encrypt and send the session key
            encrypted_session_key = server_public_key.encrypt(
                self.session_key,
                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            client_socket.sendall(encrypted_session_key)
            print("Session key sent to server")

            # Step 4: Secure communication loop
            while True:
                message = input("Enter message (type 'exit' to quit): ")
                if message.lower() == 'exit':
                    break
                encrypted_message = self.encrypt_message(message)
                client_socket.sendall(encrypted_message)
                response = client_socket.recv(1024)
                print(f"Server response: {self.decrypt_message(response)}")

    def encrypt_message(self, plaintext):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.session_key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return iv + ciphertext

    def decrypt_message(self, ciphertext):
        iv = ciphertext[:16]
        cipher = Cipher(algorithms.AES(self.session_key), modes.CFB(iv))
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext[16:]) + decryptor.finalize()
        return plaintext.decode()


if __name__ == "__main__":
    client = SecureClient(server_ip="", server_port=5000, agent_token="agent-123")
    client.start()
