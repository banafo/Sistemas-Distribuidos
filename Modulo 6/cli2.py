# Cliente de echo usando RPC
import rpyc #modulo que oferece suporte a abstracao de RPC

# endereco do servidor d echo
SERVIDOR = 'localhost'
PORTA = 10039
node = 1
neighbours = [2]


def iniciaConexao():
	'''Conecta-se ao servidor.
	Saida: retorna a conexao criada.'''
	conn = rpyc.connect(SERVIDOR, PORTA) 

	conn.root.exposed_register(node,neighbours)

	
	print(type(conn.root)) # mostra que conn.root eh um stub de cliente
	print(conn.root.get_service_name()) # exibe o nome da classe (servico) oferecido

	return conn

def fazRequisicoes(conn):
	'''Faz requisicoes ao servidor e exibe o resultado.
	Entrada: conexao estabelecida com o servidor'''
	# le as mensagens do usuario ate ele digitar 'fim'
	while True: 
		msg = input("Digite 1 para fazer eleição ('fim' para terminar):")
		if msg == 'fim': 
			break 
		elif msg == "1":# envia a mensagem do usuario para o servidor
			ret = conn.root.exposed_election(int(node))

			# imprime a mensagem recebida
			print(ret)

	# encerra a conexao
	conn.close()

def main():
	'''Funcao principal do cliente'''
	#inicia o cliente
	conn = iniciaConexao()
	#interage com o servidor ate encerrar
	fazRequisicoes(conn)

# executa o cliente
if __name__ == "__main__":
	main()