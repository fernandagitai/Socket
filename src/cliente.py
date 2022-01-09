import socket 
import threading


endereco = ("localhost", 12345)

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(endereco)

while True:
    mensagem = input("Informe texto ou digite 'sair' para desconectar: ")
    cliente_socket.send(mensagem.encode())

    if mensagem == "sair":
        cliente_socket.close()
        break
