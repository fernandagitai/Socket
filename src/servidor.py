import io
from io import FileIO
import socket 
import threading 
  
endereco = ("localhost", 12345)
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor_socket.bind(endereco)
servidor_socket.listen(1)

envio_servidor, endereco = servidor_socket.accept()
print("Nova conexao recebida de ", endereco)

while True:
    print("\nEscutando...")
    resposta = envio_servidor.recv(1024)
    resposta = resposta.rstrip().decode()

    if resposta != "sair":
        print("Mensagem do cliente:\n\n\n", resposta)
    else:
        servidor_socket.close()
        break