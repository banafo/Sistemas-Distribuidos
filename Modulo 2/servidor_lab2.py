import socket
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

#------------------------------------------------------------------------------------------------

HOST = 'localhost'   				# possibilita acessar qualquer endereco alcancavel da maquina local
PORTA = 5000  		   			# porta onde chegarao as mensagens para essa aplicacao.

sock = socket.socket() 				# cria um socket para comunicacao#
sock.bind((HOST, PORTA))			# vincula a interface e porta para comunicacao	
sock.listen(1) 					# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao



while True:												# Deixa O lado servidor iterativo
	novoSock, endereco = sock.accept() 								# aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
	print ('Conectado com: ', endereco)								# retorna um novo socket e o endereco do par conectado

	while True:
		msg_from_cliente = novoSock.recv(1024) 							# mensagem do cliente
		if not msg_from_cliente: break								
		else: 
			print("Mensagem do cliente: " + str(msg_from_cliente,  encoding='utf-8'))	# imprimir a mensagem mandando pelo cliente
			frequent_words = word_counter(str(msg_from_cliente, encoding='utf-8'))		# chamando a função word_counter para fazer o procesamento
			print(frequent_words)								# imprimir o resultado que o cliente deve receber na tela do servidor
			
			novoSock.send(bytes(frequent_words, 'UTF-8')) 	# msg_from_cliente shouldn't be changed to bytes as in cliente.py because frequent_words is already in bytes
		

novoSock.close()				# fecha o socket da conexao 
sock.close() 					# fecha o socket principal
