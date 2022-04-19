import socket

HOST = 'localhost'   # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA))
print('Digite "pare" se deseja encerra ou pode continua com a sua mensagem.\n')
while True:
	msg_to_server = input('Digite uma mensagem para servidor: ')
	if msg_to_server == 'pare':break 	#end program
	else:
		# envia uma mensagem para o par conectado
		sock.send(bytes(msg_to_server, 'UTF-8'))  #convert to bytes
		#espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
		msg_from_server = sock.recv(1024) # argumento indica a qtde maxima de bytes da mensagem
		# imprime a mensagem recebida do servidor
		print('Retorno do servidor: ' + str(msg_from_server,  encoding='utf-8'))
		
# encerra a conexao
sock.close() 

