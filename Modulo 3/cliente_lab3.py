import socket

HOST = 'localhost'   						# maquina onde esta o par passivo
PORTA = 10000       						# porta que o par passivo esta escutando

sock = socket.socket() 						# cria socket //default: socket.AF_INET, socket.SOCK_STREAM 
sock.connect((HOST, PORTA))					# conecta-se com o par passivo

print('Digite "pare" se deseja encerra ou pode continua com a sua mensagem.\n')

#----------------------------------------------------------------------------------------------------------

while True:
	msg_to_server = input('Digite o nome do arquivo para servidor: ')
	if msg_to_server == 'pare':break 							#end program
	else:
		sock.send(bytes(msg_to_server, 'UTF-8'))  					# envia uma mensagem para o par conectado //convert to bytes
		#espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
		msg_from_server = sock.recv(1024) 						# argumento indica a qtde maxima de bytes da mensagem
		print('Retorno do servidor: ' + str(msg_from_server,  encoding='utf-8')) 	# imprime a mensagem recebida do servidor
		
sock.close() 	# encerra a conexao
