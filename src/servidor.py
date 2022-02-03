import io
from io import FileIO
import socket 
import os
import threading 
  

def escolha_arquivo(conexao):

    # ENVIANDO OPÇÕES DE DOWNLOAD
    arquivos = os.listdir(os.path.join(os.getcwd(), "../dados"))
    opcoes = "Opções de download:\n"
    i = 1
    for item in arquivos:
        opcoes += str(i) + ". " + item + "\n"
        i += 1 

    try:
        conexao.sendall(str.encode(opcoes))
    except Exception as e:
        print("Erro no envio:", e)


    # OBTENDO RESPOSTA
    try:
        resposta_opcao = int(conexao.recv(1024).rstrip().decode())
        print("\nArquivo escolhido:",arquivos[resposta_opcao-1])

        arquivo_escolhido = open("./dados/" + str(arquivos[resposta_opcao-1]))
        # ENVIAR NOME, CONTEUDO E EXTENSAO
        
    except Exception as e:
        print("Erro na obtenção da opção:", e)





endereco = ("localhost", 12345)
servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

servidor_socket.bind(endereco)
servidor_socket.listen(1)

while True:
    print("\nEscutando...")

    # NOVA CONEXAO
    envio_servidor, endereco = servidor_socket.accept()
    print("\nNova conexao recebida de ", endereco)

    # ENVIANDO OPCOES DE DOWNLOAD
    escolha_arquivo(envio_servidor)

    # RECEBENDO RESPOSTA DO CLIENTE
    resposta = envio_servidor.recv(1024)
    resposta = resposta.rstrip().decode()

    if resposta != "sair":
        print("Mensagem do cliente:\n\n\n", resposta)
    else:
        servidor_socket.close()
        break