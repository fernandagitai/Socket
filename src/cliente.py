import socket
import os


def listar_arquivos(conexao):

    print()
    try:
        lista_arquivos = str(conexao.recv(4096).rstrip().decode())
        print(lista_arquivos)
        input("\nPressione enter...")

    except Exception as e:
        print("\nErro em obter opções:", e)
        return


def enviar_arquivos(conexao):
    
    # LISTANDO ARQUIVOS DISPONIVEIS PARA ENVIO 
    arquivos = os.listdir(os.path.join(os.getcwd(), "../dados cliente"))

    opcoes = "\nOpções de envio:\n"
    i = 1
    
    for item in arquivos:
        opcoes += str(i) + ". " + item + "\n"
        i += 1 
    print(opcoes)

    # ESCOLHENDO ARQUIVO A SER ENVIADO
    id_escolhido = int(input("Digite o ID do arquivo a ser enviado: "))

    
    # CONFIRMANDO ARQUIVO COM O SERVIDOR
    try:
        nome_arquivo = arquivos[id_escolhido-1]
        tamanho_arquivo = os.path.getsize("../dados cliente/" + arquivos[id_escolhido-1])

        confirmacao = str(tamanho_arquivo) + ":" + str(nome_arquivo)
        conexao.sendall(confirmacao.encode())

        print("\nEnviando o arquivo:", nome_arquivo)

    except Exception as e:
        print("Erro na escolha do arquivo:", e)
        return


    # ENVIANDO ARQUIVO
    try:
        arquivo_escolhido = open("../dados cliente/" + nome_arquivo, "rb")
        
        while True:
            arquivo_em_bytes = arquivo_escolhido.read(1024)
            if len(arquivo_em_bytes) <= 0:
                # FINALIZOU O ARQUIVO
                break
            conexao.sendall(arquivo_em_bytes)

    except Exception as e:
        print("\nErro no envio de dados:", e)
        return 

    print("\nArquivo enviado!")   
    input("Pressione enter para continuar...")



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
    try:
        file = open("../dados cliente/" + nome_arquivo, 'wb')
    except Exception as e:
        print("Erro na obtenção do arquivo:", e)
        return

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
                socket_servidor.close()
                break

            erro = listar_arquivos(socket_servidor)
            if erro:
                socket_servidor.close()
                break

        elif opcao == '2':
            try:
                socket_servidor.send("A".encode())
            except Exception as e:
                print("Erro no envio:", e)
                socket_servidor.close()
                break

            erro = enviar_arquivos(socket_servidor)
            if erro:
                socket_servidor.close()
                break

        elif opcao == '3':
            try:
                socket_servidor.send("D".encode())
            except Exception as e:
                print("Erro no envio:", e)
                socket_servidor.close()
                break

            erro = baixar_arquivos(socket_servidor)
            if erro:
                socket_servidor.close()
                break

        elif opcao == '4':
            try:
                socket_servidor.send("sair".encode())
            except Exception as e:
                print("Erro no envio:", e)

            socket_servidor.close()
            break
        else:
            print('Opção invalida!')


if __name__ == "__main__":
    cliente()