import socket
import getopt
import sys
import os
import threading


def receber_arquivos(conexao):

    # CONFIRMACAO ARQUIVO
    try:
        confirmacao = conexao.recv(4096).rstrip().decode()
        nome_arquivo = confirmacao.split(":")[-1]
        tamanho_arquivo = int(confirmacao.split(":")[0])

    except Exception as e:
        print("\nErro na confirmacao:", e)
        return

    tamanho_aux = tamanho_arquivo
    # CASO JA EXISTA UM ARQUIVO DE MESMO NOME NA PASTA
    nome_aux = nome_arquivo
    i = 1
    while os.path.exists("../dados/" + nome_aux):
        nome_aux = '(' + str(i) + ') ' + nome_arquivo
        i += 1

    nome_arquivo = nome_aux

    # BAIXANDO ARQUIVO
    with open("../dados/" + nome_arquivo, 'wb') as file:
        while True:
            if tamanho_aux <= 0:
                break

            try:
                byte = conexao.recv(1024)
                file.write(byte)
                tamanho_aux -= len(byte)

            except Exception as e:
                print("\nErro no download:", e)
                return

    print("\nArquivo adicionado com sucesso!")


def listar_arquivos(conexao):

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


def enviar_arquivos(conexao):
    arquivos = os.listdir(os.path.join(os.getcwd(), "../dados"))

    # RECEBENDO OPCAO
    try:
        resposta_opcao = int(conexao.recv(1024).rstrip().decode())
        tamanho_arquivo = os.path.getsize(
            "../dados/" + arquivos[resposta_opcao-1])
        confirmacao = str(tamanho_arquivo) + ":" + \
            str(arquivos[resposta_opcao-1])
        conexao.sendall(confirmacao.encode())

    except Exception as e:
        print("Erro no recebimento de dados:", e)
        return

    # ENVIANDO ARQUIVO
    try:
        arquivo_escolhido = open(
            "../dados/" + str(arquivos[resposta_opcao-1]), "rb")

        while True:
            arquivo_em_bytes = arquivo_escolhido.read(1024)
            if len(arquivo_em_bytes) <= 0:
                # FINALIZOU O ARQUIVO
                break
            conexao.sendall(arquivo_em_bytes)

    except Exception as e:
        print("Erro no envio de dados:", e)


def controle_cliente(conexao, endereco_cliente):

    while True:
        opcao = conexao.recv(1024).decode()

        if opcao == "A":
            receber_arquivos(conexao)

        elif opcao == "L":
            listar_arquivos(conexao)

        elif opcao == "D":
            enviar_arquivos(conexao)

        elif opcao == "sair":
            conexao.close()
            break


def servidor():

    endereco_servidor = ("localhost", 12345)
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor_socket.bind(endereco_servidor)
    servidor_socket.listen(5)

    print("\nEscutando em", endereco_servidor)

    while True:

        # NOVA CONEXAO
        conexao, endereco_cliente = servidor_socket.accept()
        print("\nNova conexao recebida de ", endereco_cliente)

        # ADICIONANDO THREAD
        thread = threading.Thread(
            target=controle_cliente, args=(conexao, endereco_cliente))
        thread.start()

        print("Conexoes ativas:", threading.active_count()-1)


if __name__ == "__main__":
    servidor()
