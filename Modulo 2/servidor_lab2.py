import socket
from collections import Counter

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

HOST = 'localhost'   
PORTA = 5000  		   


sock = socket.socket() 
sock.bind((HOST, PORTA))

sock.listen(1) 



while True:
	novoSock, endereco = sock.accept() 
	print ('Conectado com: ', endereco)

	while True:
		msg_from_cliente = novoSock.recv(1024) 
		if not msg_from_cliente: break
		else: 
			print("Mensagem do cliente: " + str(msg_from_cliente,  encoding='utf-8'))
			frequent_words = word_counter(str(msg_from_cliente, encoding='utf-8'))
			print(frequent_words)
			
			novoSock.send(bytes(frequent_words, 'UTF-8')) 	
		

novoSock.close() 


sock.close() 
