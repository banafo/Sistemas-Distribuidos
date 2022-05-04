#servidor de echo: lado servidor
#com finalizacao do lado do servidor
import socket
import select
import sys
from collections import Counter
#----------------------------------------------------------------------------------------------


# função para conta a frequencia das palavras
def word_counter(name):
	fname = name
	try:
		with open(fname,'r') as f:
			contents=f.read()
			words=contents.split()
			
		Counted = Counter(words)

		most_occur = Counted.most_common(5)

		return str(most_occur)
	except:
		return('Arquivo não encontrado')

#-----------------------------------------------------------------------------------------

# define a localizacao do servidor
HOST = 'localhost' # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
PORT = 10000 # porta de acesso

#define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]
#armazena as conexoes completadas
conexoes = {}

def iniciaServidor():
	'''Cria um socket de servidor e o coloca em modo de espera por conexoes
	Saida: o socket criado'''
	# cria o socket 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 

	# vincula a localizacao do servidor
	sock.bind((HOST, PORT))

	# coloca-se em modo de espera por conexoes
	sock.listen(5) 

	# configura o socket para o modo nao-bloqueante
	sock.setblocking(False)

	# inclui o socket principal na lista de entradas de interesse
	entradas.append(sock)

	return sock

def aceitaConexao(sock):
	'''Aceita o pedido de conexao de um cliente
	Entrada: o socket do servidor
	Saida: o novo socket da conexao e o endereco do cliente'''

	# estabelece conexao com o proximo cliente
	clisock, endr = sock.accept()

	# registra a nova conexao
	conexoes[clisock] = endr 

	return clisock, endr

def atendeRequisicoes(clisock, endr):
	'''Recebe mensagens e as envia de volta para o cliente (ate o cliente finalizar)
	Entrada: socket da conexao e endereco do cliente
	Saida: '''

	while True: 
		#recebe dados do cliente
		msg_from_cliente = clisock.recv(1024) 
		if not msg_from_cliente: # dados vazios: cliente encerrou
			print(str(endr) + '-> encerrou')
			break 
		#print(str(endr) + ': ' + str(data, encoding='utf-8'))
		print("Mensagem do cliente: " + str(msg_from_cliente,  encoding='utf-8'))
		frequent_words = word_counter(str(msg_from_cliente, encoding='utf-8'))
		clisock.send(bytes(frequent_words, 'utf-8')) # ecoa os dados para o cliente
	clisock.close() # encerra a conexao com o cliente

def main():
	'''Inicializa e implementa o loop principal (infinito) do servidor'''
	sock = iniciaServidor()
	print("Pronto para receber conexoes...")
	while True:
		#espera por qualquer entrada de interesse
		leitura, escrita, excecao = select.select(entradas, [], [])
		#tratar todas as entradas prontas
		for pronto in leitura:
			if pronto == sock:  #pedido novo de conexao
				clisock, endr = aceitaConexao(sock)
				print ('Conectado com: ', endr)
				atendeRequisicoes(clisock, endr)
			elif pronto == sys.stdin: #entrada padrao
				cmd = input()
				if cmd == 'fim': #solicitacao de finalizacao do servidor
					sock.close()
					sys.exit()
				elif cmd == 'hist': #outro exemplo de comando para o servidor
					print(str(conexoes.values()))

main()
