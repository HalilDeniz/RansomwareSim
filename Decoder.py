import gc
import socket
import json
import os
from cryptography.fernet import Fernet

class Decoder:
    def __init__(self, directory, server_host, server_port):
        self.directory = directory
        self.server_host = server_host
        self.server_port = server_port

    def decrypt_file(self, file_path, key):
        fernet = Fernet(key)
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data)

        original_file_path = file_path.replace(".denizhalil", "")
        with open(original_file_path, 'wb') as file:
            file.write(decrypted_data)

        os.remove(file_path)

    def find_and_decrypt_files(self, key):
        for root, _, files in os.walk(self.directory):
            for file in files:
                if file.endswith(".denizhalil"):
                    file_path = os.path.join(root, file)
                    self.decrypt_file(file_path, key)

    def request_key_from_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.server_host, self.server_port))
            s.sendall(json.dumps({'request': 'key'}).encode())
            data = s.recv(1024)
            response = json.loads(data.decode())
            return response.get('key')

    def delete_readme(self):

        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        readme_path = os.path.join(desktop_path, 'Readme.txt')

        if os.path.exists(readme_path):
            os.remove(readme_path)
        else:
            pass

    def clear_memory(self):
        gc.collect()
        print("Memory cleared.")
def main():
    directory = 'dosyalar/'  # Replace with the target directory path
    server_host = '10.0.2.37'
    server_port = 12345
    print("Waiting for key...")

    try:
        decoder = Decoder(directory, server_host, server_port)
        key = decoder.request_key_from_server()

        if key:
            decoder.find_and_decrypt_files(key)
            print("Files successfully decrypted.")
            decoder.delete_readme()
        else:
            print("Key not found or incorrect.")
    except Exception as e:
        print(f"An error occurred: {e}\nPlease restart the program.")

    decoder.clear_memory()

if __name__ == "__main__":
    main()
