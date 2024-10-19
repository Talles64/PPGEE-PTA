import socket
import threading
import os
import base64

class PTA:
    def __init__(self, host, port, buffer_size, users_file, files_dir):
        self.server_host = host
        self.server_port = port
        self.buffer_size = buffer_size
        self.users_file = users_file
        self.files_dir = files_dir
        self.valid_users = self.load_users()  

    # Carrega os usuários válidos a partir do arquivo configurado
    def load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                return [line.strip().lower() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Arquivo {self.users_file} não encontrado.")
            return []

    # Lista os arquivos disponíveis no diretório de arquivos
    def list_files(self):
        try:
            files = os.listdir(self.files_dir)
            return [f for f in files if os.path.isfile(os.path.join(self.files_dir, f))]
        except Exception as e:
            print(f"Erro ao listar arquivos: {e}")
            return []

    # gerencia a conexão de cada cliente
    def handle_client(self, client_socket, client_address):
        print(f"Conexão estabelecida com {client_address}")
        state = 'AWAITING_CUMP'
        current_user = None

        try:
            while True:
                data = client_socket.recv(self.buffer_size)
                if not data:
                    print(f"Conexão encerrada por {client_address}")
                    break

                message = data.decode().strip()
                print(f"Recebido de {client_address}: {message}")

                seq_num, command, args = self.parse_message(message)
                
                if state == 'AWAITING_CUMP':
                    state = self.handle_cump(client_socket, seq_num, command, args)
                elif state == 'READY':
                    if command == 'LIST':
                        self.handle_list(client_socket, seq_num)
                    elif command == 'PEGA':
                        self.handle_pega(client_socket, seq_num, args)
                    elif command == 'TERM':
                        self.handle_term(client_socket, seq_num)
                        break
                    else:
                        self.send_response(client_socket, seq_num, "NOK")

        except Exception as e:
            print(f"Erro com {client_address}: {e}")
        finally:
            client_socket.close()

    # formata a msg
    def parse_message(self, message):
        parts = message.split(' ', 2)
        seq_num = parts[0] if len(parts) > 0 else '0'
        command = parts[1].upper() if len(parts) > 1 else ''
        args = parts[2] if len(parts) > 2 else ''
        return seq_num, command, args

    # gerencia CUMP
    def handle_cump(self, client_socket, seq_num, command, username):
        if command == 'CUMP' and username.lower() in self.valid_users:
            self.send_response(client_socket, seq_num, "OK")
            return 'READY'
        else:
            self.send_response(client_socket, seq_num, "NOK")
            return 'AWAITING_CUMP'

    # gerencia LIST
    def handle_list(self, client_socket, seq_num):
        files = self.list_files()
        if files:
            files_str = ",".join(files)
            self.send_response(client_socket, seq_num, "ARQS", f"{len(files)} {files_str}")
        else:
            self.send_response(client_socket, seq_num, "NOK")

    # gerencia PEGA
    def handle_pega(self, client_socket, seq_num, filename):
        filepath = os.path.join(self.files_dir, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'rb') as f:
                    file_data = f.read()
                file_data_base64 = base64.b64encode(file_data).decode('ascii').replace('\n', '')
                file_size = len(file_data_base64)
                self.send_response(client_socket, seq_num, "ARQ", f"{file_size} {file_data_base64}")
                print(f"Arquivo {filename} enviado para o cliente.")
            except Exception as e:
                print(f"Erro ao enviar arquivo: {e}")
                self.send_response(client_socket, seq_num, "NOK")
        else:
            self.send_response(client_socket, seq_num, "NOK")

    # gerencia TERM
    def handle_term(self, client_socket, seq_num):
        self.send_response(client_socket, seq_num, "OK")
        print("Conexão encerrada pelo cliente.")

    # formata response
    def send_response(self, client_socket, seq_num, reply, args=''):
        response = f"{seq_num} {reply} {args}" if args else f"{seq_num} {reply}"
        client_socket.sendall(response.encode())
        print(f"Enviado para cliente: {response.strip()}")

    # inicia o server
    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_host, self.server_port))
        server.listen(5)
        print(f"Servidor PTA ouvindo em {self.server_host}:{self.server_port}")

        try:
            while True:
                client_socket, client_address = server.accept()
                client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                client_handler.start()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")
        finally:
            server.close()

if __name__ == "__main__":
    pta_server = PTA(
        host='0.0.0.0', 
        port=11550, 
        buffer_size=4096, 
        users_file=r'pta-server\users.txt', 
        files_dir=r'pta-server\files'
    )
    pta_server.start_server()
