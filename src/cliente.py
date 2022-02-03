import io
from io import FileIO
import socket 
import threading

def escolha_arquivo_cliente(cliente_socket):

    # EXIBINDO AS OPÇÕES DE DOWNLOAD
    print()
    try:
        opcoes = str(cliente_socket.recv(4096).rstrip().decode())
        no_opcoes = len(opcoes.split("\n")) - 1
        print(opcoes)
    except Exception as e:
        print("\nErro em obter opções:", e)
        return

    # ENVIANDO A OPÇÃO ESCOLHIDA
    while True:
        escolha = int(input("\nDigite o ID do arquivo a ser baixado: "))
        if escolha <= no_opcoes and escolha > 0:
            try:
                cliente_socket.send(str(escolha).encode())
                return 

            except Exception as e:
                print("\nErro em obter opções:", e)
                continuar = input("\nDeseja digitar novamente? s/n: ")
                if continuar == "n":
                    return

        else:
            print("\nNúmero inválido.")
            continuar = input("Deseja digitar novamente? s/n: ")
            if continuar == "n":
                return






endereco = ("localhost", 12345)

cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect(endereco)

escolha_arquivo_cliente(cliente_socket)


while True:
    mensagem = input("\nInforme texto ou digite 'sair' para desconectar: ")

    if mensagem == "sair":
        cliente_socket.send(mensagem.encode())
        cliente_socket.close()
        break
    
    else:
        arquivo = open("../dados/"+mensagem, encoding="UTF-8")
        cliente_socket.send(arquivo.read().encode())
        arquivo.close()
