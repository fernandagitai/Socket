import io
from io import FileIO
import socket 
import threading


endereco = ("localhost", 12345)

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(endereco)

while True:
    mensagem = input("Informe texto ou digite 'sair' para desconectar: ")

    if mensagem == "sair":
        cliente_socket.send(mensagem.encode())
        cliente_socket.close()
        break
    
    else:
        arquivo = open("../dados/"+mensagem, encoding="UTF-8")
        cliente_socket.send(arquivo.read().encode())
        arquivo.close()
