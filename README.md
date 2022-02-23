# ✔️ PROJETO SOCKETS

Projeto da disciplina Redes de Computadores (UFAL), ministrada pelo professor Leandro de Sales, o qual se trata da implementação de aplicação em redes por meio de sockets.

Alunas:

- Leticia Gabriela Cena de Lima
- Maria Fernanda Herculano Machado da Silva

## Principais funcionalidades ✨

A aplicação desenvolvida foi seguindo o modelo de Cliente-Servidor. Seu principal objetivo é a transferência de arquivos, tanto do servidor com o cliente quanto o caminho contrário.  
Na aplicação, um hospedeiro precisa ser o servidor centralizado, que armazena dados e vai lidar com as requisições de múltiplos clientes. Estes, podem fazer upload de outros arquivos para o servidor ou fazer download dos arquivos que já estão lá.  
A aplicação possui 4 opções para o cliente escolher:

1. Listar arquivos no servidor.
2. Enviar arquivo.
3. Baixar arquivo.
4. Sair.

A primeira opção irá mostrar quais os arquivos que estão presentes no servidor, que estão disponíveis para serem baixados pelos clientes.  
A segunda tem a função de enviar um arquivo que está na pasta do cliente para o servidor.  
A terceira vai possibilitar que o cliente baixe um arquivo que está salvo no servidor (algum dos que foram mostrados pela função 1) para sua pasta pessoal.  
Por último, tem a opção de sair, que fará um _logoff_ do cliente, removendo sua conexão com o servidor.

## O que poderia ter sido adicionado 🤔

Algumas outras funcionalidade poderiam ter sido implementadas, como a opção de deletar um arquivo, baixar mais de um arquivo por vez, conseguir fazer compactação de arquivos na hora de baixar e até mesmo uma interface que deixasse a conexão com o cliente mais intuitiva e mais fácil.

## Dificuldades durante a implementação 😥

Dificuldade no começo para lidar com a implementação das threads e conseguir conectar mais de um cliente simultaneamente. Também houve dificuldade na hora de enviar o arquivo, tanto no caminho servidor-cliente quanto no contrário, pois chegava apenas um arquivo vazio.  
Mas com algumas leituras e pesquisas, os problemas foram resolvidos e as funções foram implementadas.

## Como executar? 💻

A aplicação foi desenvolvida na linguagem Python, portanto é preciso que na máquina que deseje executar exista uma versão recente do Python, e.g. 3.9.x.  
Para executar, é preciso baixar o repositório e abrir a pasta "src".  
Feito isso, abrir o terminal na mesma pasta e executar o comando:

```
$ python3 servidor.py
```

Assim, o servidor já estará conectado e pronto para receber os comandos do cliente.  
Para que o cliente possa começar a interagir com o servidor é executado o seguinte comando:

```
$ python3 cliente.py
```

Irá abrir uma lista de opções que o cliente poderá escolher: listar os arquivos do servidor, baixar e enviar arquivos.  
Por causa do uso de thread, é possível que mais de um cliente se conecte ao servidor ao mesmo tempo, para testar isso é só repetir o último passo em outra aba do terminal.
