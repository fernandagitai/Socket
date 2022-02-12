import socket
import getopt
import sys
import os


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


def listar_arquivos(conexao):

    print()
    try:
        lista_arquivos = str(conexao.recv(4096).rstrip().decode())
        print(lista_arquivos)
        input("Pressione enter...")

    except Exception as e:
        print("\nErro em obter opções:", e)


def enviar_arquivos(conexao):
    pass


def baixar_arquivos(conexao):
    
    # COMANDO
    print()
    id_escolhido = input("Digite o ID do arquivo escolhido (disponiveis na listagem): ")
    
    # ENVIANDO OPCAO
    try:
        conexao.send(id_escolhido.encode())

    except Exception as e:
        print("\nErro no envio:", e)
        return

    # CONFIRMACAO ARQUIVO
    try:
        confirmacao = conexao.recv(4096).rstrip().decode()
        nome_arquivo = confirmacao.split(":")[-1]
        tamanho_arquivo = int(confirmacao.split(":")[0])
        
        print(nome_arquivo)

    except Exception as e:
        print("\nErro na confirmacao:", e)
        return  

    # CASO JA EXISTA UM ARQUIVO DE MESMO NOME NA PASTA
    nome_aux = nome_arquivo
    i = 1
    while os.path.exists("./dados cliente/" + nome_aux):
        nome_aux = '(' + str(i) + ')' + nome_arquivo
        i += 1

    nome_arquivo = nome_aux
    tamanho_aux = tamanho_arquivo

    # BAIXANDO ARQUIVO
    with open("../dados cliente/" + nome_arquivo, 'wb') as file:
        while True:
            if tamanho_aux <= 0:
                break

            try:
                byte = conexao.recv(1024)
                file.write(byte)
                tamanho_aux -= len(byte)

            except Exception as e:
                print("Erro no download:", e)
                return

    print("Arquivo baixado!")

            

def cliente():

    endereco = ("localhost", 12345)

    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.connect(endereco)

    while True:

        # MENU
        print('\n[1] Listar arquivos\n[2] Enviar arquivo\n[3] Receber arquivo\n[4] Sair\n')
        opcao = input("Opcao: ")
        
        if opcao == '1':
            try:
                socket_servidor.send("L".encode())
            except Exception as e:
                print("Erro no envio:", e)

            listar_arquivos(socket_servidor)

        elif opcao == '2':
            try:
                socket_servidor.send("A".encode())
            except Exception as e:
                print("Erro no envio:", e)

            enviar_arquivos(socket_servidor)

        elif opcao == '3':
            try:
                socket_servidor.send("D".encode())
            except Exception as e:
                print("Erro no envio:", e)

            baixar_arquivos(socket_servidor)

        elif opcao == '4':
            try:
                socket_servidor.send("sair".encode())
            except Exception as e:
                print("Erro no envio:", e)

            socket_servidor.close()
            break
        else:
            print('Opção invalida!')

        
        
        
        # mensagem = input("\nInforme texto ou digite 'sair' para desconectar: ")
        # else:
        #     arquivo = open("../dados/"+mensagem, encoding="UTF-8")
        #     cliente_socket.send(arquivo.read().encode())
        #     arquivo.close()

if __name__ == "__main__":
    cliente()